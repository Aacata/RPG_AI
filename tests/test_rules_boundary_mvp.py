from __future__ import annotations

import unittest

from src.core.contracts import (
    EventCategory,
    MutationKind,
    SlotKey,
    TargetKind,
)
from src.core.ids import make_actor_id
from src.core.state_root import StateRoot
from src.npc.actor_baseline import ActorRecord
from src.rules.boundary import inspect_rules_action, process_rules_action
from src.rules.contracts import RulesActionRequest


class RulesBoundaryMvpTests(unittest.TestCase):
    def test_accepted_set_actor_current_activity(self) -> None:
        actor_id = make_actor_id("guard")
        state_root = StateRoot(
            actors={
                str(actor_id): ActorRecord(
                    actor_id=actor_id,
                    display_name="Guard",
                )
            }
        )
        request = RulesActionRequest(
            request_id="req_1",
            action_kind="set_actor_current_activity",
            actor_id=actor_id,
            activity="standing_guard",
        )

        inspection = inspect_rules_action(state_root, request)

        self.assertEqual(inspection.status, "accepted")
        self.assertEqual(inspection.diagnostics, ())
        self.assertIsNotNone(inspection.proposed_change)
        self.assertIsNotNone(inspection.event_handoff)

        proposed_change = inspection.proposed_change
        assert proposed_change is not None
        self.assertEqual(proposed_change.proposal_id, "req_1")
        self.assertEqual(proposed_change.intent_type, "rules.set_actor_current_activity")
        self.assertEqual(
            proposed_change.target_refs,
            (proposed_change.requested_changes[0].target,),
        )
        self.assertEqual(len(proposed_change.requested_changes), 1)

        mutation = proposed_change.requested_changes[0]
        self.assertEqual(mutation.change_id, "req_1")
        self.assertEqual(mutation.mutation_kind, MutationKind.SET_VALUE)
        self.assertEqual(mutation.target.kind, TargetKind.ACTOR)
        self.assertEqual(mutation.target.record_id, str(actor_id))
        self.assertEqual(
            mutation.arguments,
            {
                "slot_key": SlotKey.CURRENT_ACTIVITY.value,
                "value": "standing_guard",
            },
        )
        self.assertEqual(mutation.preconditions, {})

        updated_state, events, diagnostics = process_rules_action(state_root, request)

        self.assertEqual(diagnostics, ("ProposedChange accepted.",))
        self.assertEqual(
            updated_state.actors[str(actor_id)].current_activity,
            "standing_guard",
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].category, EventCategory.RULES_OUTCOME)
        self.assertEqual(
            events[0].payload,
            {
                "action_kind": "set_actor_current_activity",
                "activity": "standing_guard",
            },
        )

    def test_rejected_when_actor_reference_is_unknown(self) -> None:
        actor_id = make_actor_id("missing")
        state_root = StateRoot()
        request = RulesActionRequest(
            request_id="req_missing",
            action_kind="set_actor_current_activity",
            actor_id=actor_id,
            activity="standing_guard",
        )

        inspection = inspect_rules_action(state_root, request)

        self.assertEqual(inspection.status, "rejected")
        self.assertEqual(inspection.diagnostics, ("Unknown actor reference.",))
        self.assertIsNone(inspection.proposed_change)
        self.assertIsNone(inspection.event_handoff)

        returned_state, events, diagnostics = process_rules_action(state_root, request)

        self.assertIs(returned_state, state_root)
        self.assertEqual(events, ())
        self.assertEqual(diagnostics, ("Unknown actor reference.",))

    def test_rejected_when_activity_is_whitespace_only(self) -> None:
        actor_id = make_actor_id("guard")
        state_root = StateRoot(
            actors={
                str(actor_id): ActorRecord(
                    actor_id=actor_id,
                    display_name="Guard",
                )
            }
        )
        request = RulesActionRequest(
            request_id="req_blank_activity",
            action_kind="set_actor_current_activity",
            actor_id=actor_id,
            activity="   ",
        )

        inspection = inspect_rules_action(state_root, request)

        self.assertEqual(inspection.status, "rejected")
        self.assertEqual(
            inspection.diagnostics,
            ("Activity must be a non-empty string.",),
        )
        self.assertIsNone(inspection.proposed_change)
        self.assertIsNone(inspection.event_handoff)

        returned_state, events, diagnostics = process_rules_action(state_root, request)

        self.assertIs(returned_state, state_root)
        self.assertEqual(events, ())
        self.assertEqual(
            diagnostics,
            ("Activity must be a non-empty string.",),
        )


if __name__ == "__main__":
    unittest.main()
