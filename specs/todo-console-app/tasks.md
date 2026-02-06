---
description: "Task list for Evolution of Todo Console Application implementation"
---

# Tasks: Evolution of Todo Console Application

**Input**: Design documents from `/specs/todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Constitution Compliance**: All tasks must follow Spec-Driven Development and Test-First principles as defined in the project constitution

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Constitution Compliance Requirements

1. **Spec-Driven Development**: All code changes must be based on specification updates; no manual coding without spec updates
2. **Test-First Approach**: Write tests before implementation; ensure tests fail before writing implementation code
3. **Clean Architecture**: Follow single-responsibility functions with clear naming
4. **Data Constraints**: No persistence to file system or database; data exists only during runtime

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure under /src with main.py and task_manager.py
- [ ] T002 Initialize Python project with basic configuration
- [ ] T003 [P] Set up basic directory structure for src/ and tests/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Foundational tasks for the todo application:

- [ ] T004 Define Task data model in src/task_manager.py with id, title, description, completed fields
- [ ] T005 [P] Implement TaskManager class with in-memory storage in src/task_manager.py
- [ ] T006 Create main application loop structure in src/main.py
- [ ] T007 Implement unique ID generation for tasks in src/task_manager.py
- [ ] T008 Set up basic CLI menu structure in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks to their todo list with a title and optional description

**Independent Test**: The user can run the application and add a task with a title, and see it appear in the task list.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for add_task functionality in tests/unit/test_task_manager.py
- [ ] T010 [P] [US1] Integration test for adding task via CLI in tests/integration/test_cli.py

### Implementation for User Story 1

- [ ] T011 [P] [US1] Implement add_task method in src/task_manager.py
- [ ] T012 [US1] Add input validation for task title in src/task_manager.py
- [ ] T013 [US1] Implement CLI menu option for adding tasks in src/main.py
- [ ] T014 [US1] Add error handling for empty title in src/task_manager.py
- [ ] T015 [US1] Set default completion status to False when adding tasks in src/task_manager.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: Allow users to view all their tasks with their status

**Independent Test**: The user can run the application, add a task, and then view the list to see the task displayed with its ID and status.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Unit test for view_tasks functionality in tests/unit/test_task_manager.py
- [ ] T017 [P] [US2] Integration test for viewing tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 2

- [ ] T018 [P] [US2] Implement view_tasks method in src/task_manager.py
- [ ] T019 [US2] Create formatted display for tasks in src/task_manager.py
- [ ] T020 [US2] Implement CLI menu option for viewing tasks in src/main.py
- [ ] T021 [US2] Handle empty task list case in src/task_manager.py
- [ ] T022 [US2] Display ID, title, and completion status for each task in src/task_manager.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: Allow users to update the details of a task

**Independent Test**: The user can update an existing task's title or description by providing the task ID.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Unit test for update_task functionality in tests/unit/test_task_manager.py
- [ ] T024 [P] [US3] Integration test for updating tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 3

- [ ] T025 [P] [US3] Implement update_task method in src/task_manager.py
- [ ] T026 [US3] Add validation for task ID existence in src/task_manager.py
- [ ] T027 [US3] Implement CLI menu option for updating tasks in src/main.py
- [ ] T028 [US3] Preserve completion status when updating tasks in src/task_manager.py
- [ ] T029 [US3] Handle invalid task ID gracefully in src/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Allow users to remove tasks that they no longer need

**Independent Test**: The user can delete an existing task by providing its ID, and the task is removed from the list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US4] Unit test for delete_task functionality in tests/unit/test_task_manager.py
- [ ] T031 [P] [US4] Integration test for deleting tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 4

- [ ] T032 [P] [US4] Implement delete_task method in src/task_manager.py
- [ ] T033 [US4] Add validation for task ID existence in src/task_manager.py
- [ ] T034 [US4] Implement CLI menu option for deleting tasks in src/main.py
- [ ] T035 [US4] Handle invalid task ID gracefully in src/task_manager.py
- [ ] T036 [US4] Update task list display after deletion in src/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Complete / Incomplete (Priority: P5)

**Goal**: Allow users to mark tasks as complete or incomplete

**Independent Test**: The user can toggle the completion status of a task by providing its ID.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US5] Unit test for toggle_task_status functionality in tests/unit/test_task_manager.py
- [ ] T038 [P] [US5] Integration test for toggling task status via CLI in tests/integration/test_cli.py

### Implementation for User Story 5

- [ ] T039 [P] [US5] Implement toggle_task_status method in src/task_manager.py
- [ ] T040 [US5] Add validation for task ID existence in src/task_manager.py
- [ ] T041 [US5] Implement CLI menu option for toggling task status in src/main.py
- [ ] T042 [US5] Handle invalid task ID gracefully in src/task_manager.py
- [ ] T043 [US5] Update display to reflect status changes in src/task_manager.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: CLI Integration & Polish

**Purpose**: Complete the CLI menu and integrate all features

- [ ] T044 [P] Complete main menu with all options in src/main.py
- [ ] T045 Implement proper input validation and error handling in src/main.py
- [ ] T046 Add graceful exit functionality in src/main.py
- [ ] T047 [P] Add comprehensive error messages for invalid inputs in src/main.py
- [ ] T048 Implement user-friendly prompts and instructions in src/main.py

---

## Phase 9: Verification & Testing

**Purpose**: Validate the complete application against specifications

- [ ] T049 Run complete application flow test to verify all features work together
- [ ] T050 [P] Test error handling for all edge cases in src/task_manager.py
- [ ] T051 Validate behavior against original specifications
- [ ] T052 Perform manual testing of all menu options
- [ ] T053 Verify no manual code edits were made outside of Claude Code generation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **CLI Integration (Phase 8)**: Depends on all user stories being complete
- **Verification (Phase 9)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Core functionality before UI/cli integration
- Validation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence