1. Design Considerations & Tradeoffs
User Flows & Cross-Boundary Data
The Studio Interface: A centralized React-based workspace. The primary design choice is to use a Global Dashboard Tray or a standalone Custom Page (/studio). A standalone page is preferred to provide more screen real estate for editing documents and videos.

    Data Crossing Boundaries:
        External to Internal: "Import" features will pull from the user’s local machine or Canvas Files into the Studio buffer.

        Internal to Submission: Data moves from the Studio state to the SubmissionsController via the POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions endpoint.

        UX Risks: The "Are you sure?" popup must be high-contrast and non-dismissible by clicking outside the modal to prevent accidental submissions of unfinished drafts.

        Feature Interaction (Canvas Concepts)
        Roles: The Studio is visible only to Student and Observer roles.

        Assignments: The dropdown must filter out quiz and external_tool types if they don't support standard file/text submissions.

2. Functional Requirements
"The System Shall..."
    Requirement 1: Aggregate all active, submittable assignments across all user enrollments into a single searchable dropdown.

    Requirement 2: Display the assignment's description and due_at timestamp within a confirmation modal upon selection.

    Requirement 3: Allow users to switch between assignments in the dropdown without clearing the current content in the "Studio" editor.

    Requirement 4: Post the completed work to the Canvas Submissions API and return a success receipt (JSON response).

    Boundaries
        In Scope: Text entry, file uploads (PDF/DocX/Images), and media imports.
        Out of Scope: Peer reviews, LTI tool submissions, and offline-only assignments.

3. Non-Functional Requirements
    Performance: Assignment aggregation must happen asynchronously to prevent page-load blocking.

    Security (FERPA): Submissions must strictly follow existing Canvas ACLs (Access Control Lists). The Studio cannot "see" assignments in courses where the user is not an active student.

    Observability: Implement client-side logging for submission "Intent" vs. "Success" to track if users are abandoning the process at the popup stage.

    Accessibility: The assignment dropdown must support ARIA-live regions to announce the selection of a new assignment to screen readers.

4. Codebase Analysis (via Lab 2 Agent)
    Hypotheses
        UI: Primary frontend work will occur in app/jsx using Instructure UI components.

        API: A new endpoint may be needed in app/controllers/api/v1/ to fetch "all submittable assignments" in one call, rather than iterating through every course.

    Concrete Findings
        Pattern to Follow: The DashboardPresenter in app/presenters/ already handles gathering "To-Do" items across courses. I will extend this logic for the Studio dropdown.

        Subsystem: app/models/assignment.rb contains the published? and locked_for? logic which must be checked before showing an assignment in the Studio.

        Extension Point: The global navigation sidebar can be extended via app/views/shared/_menu_items.html.erb or via a JavaScript-injected tray.

    Open Questions
        Persistence: If a student closes the browser, should the Studio draft be saved to a draft_submissions table or browser localStorage? (Requires a "spike" on database migration costs).

5. Testing and Verification Plan
    Unit-Level Expectations
        Logic Test: Ensure the assignment filter correctly excludes "Closed" assignments.

        Validation Test: Ensure the "Submit" button remains disabled if the Studio editor is empty.

    Integration Points
        API Verification: Use RSpec to verify that calling the Studio submission logic triggers a Version creation in the Submissions table.

        Database: Confirm that Attachments uploaded via the Studio are correctly linked to the resulting Submission object.

    Manual / Exploratory Checks
        Role Check: Log in as a Teacher and verify the "Studio" link is hidden or provides a "Student View" warning.

        Edge Case: Select an assignment in the dropdown, have a Teacher "Unpublish" that assignment in another tab, then attempt to submit. Verify the system handles the 404/401 error gracefully.

    Acceptance Criteria 
        Dropdown Context: Manually verify that assignments from Course A and Course B both appear.

        Safety Popup: Verify the "Are you sure?" modal appears and contains the correct assignment title.

        Submission: Verify the "Submission Received" confetti/notification triggers and the file appears in the Gradebook.