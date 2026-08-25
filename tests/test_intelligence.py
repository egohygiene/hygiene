from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import intelligence  # noqa: E402


class RepositoryIntelligenceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot = intelligence.load_json(
            ROOT / "fixtures" / "repository-intelligence" / "complete-quest.json"
        )
        cls.vocabulary = intelligence.load_json(
            ROOT / "catalog" / "repository-intelligence-vocabulary.json"
        )

    def test_contract_schemas_are_valid_json_schema_documents(self) -> None:
        for name in (
            "repository-intelligence.v1.schema.json",
            "repository-intelligence-vocabulary.v1.schema.json",
        ):
            schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
            self.assertEqual(
                "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
            )
            self.assertTrue(schema["$id"].startswith("https://egohygiene.io/"))

    def test_checked_in_vocabulary_is_valid(self) -> None:
        self.assertEqual([], intelligence.validate_vocabulary(self.vocabulary))

    def test_contracts_are_registered_as_proposals(self) -> None:
        index = intelligence.load_json(ROOT / "catalog" / "contracts.yaml")
        contracts = {contract["id"]: contract for contract in index["contracts"]}
        for contract_id in (
            intelligence.SCHEMA,
            intelligence.VOCABULARY_SCHEMA,
        ):
            self.assertEqual("proposed", contracts[contract_id]["status"])
            self.assertEqual("egohygiene/hygiene", contracts[contract_id]["owner"])

    def test_complete_quest_fixture_is_valid(self) -> None:
        self.assertEqual(
            [], intelligence.validate_snapshot(self.snapshot, self.vocabulary)
        )

    def test_complete_quest_covers_intent_through_deployment(self) -> None:
        kinds = {entity["kind"] for entity in self.snapshot["entities"]}
        self.assertEqual(set(intelligence.ENTITY_KIND_TO_ID), kinds)
        relationship_types = {
            relationship["type"] for relationship in self.snapshot["relationships"]
        }
        self.assertTrue(
            {
                "depends-on",
                "deploys",
                "evidences",
                "implements",
                "informs",
                "releases",
                "tracks",
                "verifies",
            }.issubset(relationship_types)
        )
        event_types = {event["type"] for event in self.snapshot["events"]}
        self.assertTrue(
            {
                "roadmap_step.status_changed",
                "architecture_decision.accepted",
                "issue.closed",
                "pull_request.merged",
                "commit.created",
                "check.completed",
                "release.published",
                "deployment.completed",
            }.issubset(event_types)
        )

    def test_duplicate_entity_id_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.snapshot)
        candidate["entities"].append(copy.deepcopy(candidate["entities"][0]))
        errors = intelligence.validate_snapshot(candidate, self.vocabulary)
        self.assertTrue(
            any("duplicate id" in error for error in errors),
            errors,
        )

    def test_missing_and_dangling_provenance_are_rejected(self) -> None:
        missing = copy.deepcopy(self.snapshot)
        missing["entities"][0]["provenance"] = []
        errors = intelligence.validate_snapshot(missing, self.vocabulary)
        self.assertTrue(any("at least one source id" in error for error in errors))

        dangling = copy.deepcopy(self.snapshot)
        dangling["relationships"][0]["provenance"] = ["source:not-real"]
        errors = intelligence.validate_snapshot(dangling, self.vocabulary)
        self.assertTrue(any("unknown source source:not-real" in error for error in errors))

    def test_public_snapshot_rejects_non_public_members(self) -> None:
        candidate = copy.deepcopy(self.snapshot)
        candidate["sources"][0]["visibility"] = "private"
        errors = intelligence.validate_snapshot(candidate, self.vocabulary)
        self.assertTrue(any("exceeds snapshot visibility public" in error for error in errors))

    def test_relationship_endpoint_kinds_follow_vocabulary(self) -> None:
        candidate = copy.deepcopy(self.snapshot)
        deployment = next(
            entity["id"]
            for entity in candidate["entities"]
            if entity["kind"] == "deployment"
        )
        candidate["relationships"][0]["source"] = deployment
        errors = intelligence.validate_snapshot(candidate, self.vocabulary)
        self.assertTrue(
            any(
                "source kind deployment is invalid for informs" in error
                for error in errors
            )
        )

    def test_snapshot_can_reference_provenance_backed_external_entities(self) -> None:
        candidate = copy.deepcopy(self.snapshot)
        external_source = copy.deepcopy(candidate["sources"][-1])
        external_source.update(
            {
                "id": "source:hygiene-contract",
                "repository": "egohygiene/hygiene",
                "url": (
                    "https://github.com/egohygiene/hygiene/blob/"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/README.md"
                ),
            }
        )
        candidate["sources"].append(external_source)
        candidate["sources"].sort(key=lambda item: item["id"])

        external_entity = {
            "id": "ri:egohygiene/hygiene:repository:egohygiene/hygiene",
            "kind": "repository",
            "repository": "egohygiene/hygiene",
            "key": "egohygiene/hygiene",
            "title": "Hygiene",
            "canonical_url": "https://github.com/egohygiene/hygiene",
            "visibility": "public",
            "state": {"value": "active", "assertion": "authoritative"},
            "freshness": "current",
            "provenance": ["source:hygiene-contract"],
            "attributes": {"default_branch": "main"},
            "extensions": {},
        }
        candidate["entities"].append(external_entity)
        candidate["entities"].sort(key=lambda item: item["id"])

        root = "ri:egohygiene/relay:repository:egohygiene/relay"
        candidate["relationships"].append(
            {
                "id": "relationship:relay-depends-hygiene",
                "type": "depends-on",
                "source": root,
                "target": external_entity["id"],
                "direction": "directed",
                "assertion": "authoritative",
                "freshness": "current",
                "provenance": ["source:hygiene-contract", "source:roadmap"],
                "extensions": {},
            }
        )
        candidate["relationships"].sort(key=lambda item: item["id"])
        self.assertEqual(
            [], intelligence.validate_snapshot(candidate, self.vocabulary)
        )

    def test_dependency_cycle_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.snapshot)
        dependency = next(
            relationship
            for relationship in candidate["relationships"]
            if relationship["type"] == "depends-on"
        )
        reverse = copy.deepcopy(dependency)
        reverse["id"] = "relationship:foundation-depends-quest"
        reverse["source"], reverse["target"] = reverse["target"], reverse["source"]
        candidate["relationships"].append(reverse)
        candidate["relationships"].sort(key=lambda item: item["id"])
        errors = intelligence.validate_snapshot(candidate, self.vocabulary)
        self.assertIn("relationships contain a depends-on cycle", errors)

    def test_contract_order_and_diagnostics_are_deterministic(self) -> None:
        candidate = copy.deepcopy(self.snapshot)
        candidate["events"][0], candidate["events"][1] = (
            candidate["events"][1],
            candidate["events"][0],
        )
        first = intelligence.validate_snapshot(candidate, self.vocabulary)
        second = intelligence.validate_snapshot(copy.deepcopy(candidate), self.vocabulary)
        self.assertEqual(first, second)
        self.assertIn("snapshot.events must use stable contract order", first)


if __name__ == "__main__":
    unittest.main()
