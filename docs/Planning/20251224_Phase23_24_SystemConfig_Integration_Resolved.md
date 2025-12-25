# Phase 23: System Config Integration & UI Synchronization (RESOLVED)

## Goal
Replace the hardcoded dummy settings in the `/settings` page with a dynamic UI that reads from and writes to the backend's `system_config.json`. This empowers the user to tune critical system behaviors (OCR parameters, Image Processing, Model Priority) directly from the application without editing JSON files.

## Technical Architecture

### Backend (`app/api/v1/endpoints/settings.py`)
- **API Expansion**: Functionality already exists (`get_system_config`, `update_system_config`), but needs verification against the Pydantic schema.
- **Validation**: Ensure `app/schemas/config.py` accurately reflects `system_config.json` structure to prevent data corruption.
- **Hot-Reload**: Verify `ConfigService` reloads the file from disk or updates the in-memory state immediately upon save.

### Frontend (`app/settings/page.tsx`)
- **Data Fetching**: Use `SettingsAPI.getSystemConfig()` to load initial state.
- **State Management**: Use `React Hook Form` or local state to manage form changes before saving.
- **Dynamic UI Components**:
    - **Toggles**: For boolean flags (e.g., `to_grayscale`, `remove_noise`).
    - **Sliders/Inputs**: For numeric thresholds (e.g., `contrast_factor`).
    - **Reorderable List**: For `model_priority` to allowing dragging or moving items up/down.
    - **JSON Editor (Advanced)**: Optional fall-back for complex nested structures like prompts.

## Changes Implemented

### Backend
- [x] **Schema Validation**: Audited and fixed `SystemConfig` Pydantic model (added `_model_priority_rule`).
- [x] **API Logic**: Verified `PUT /config` writes safely to `system_config.json`.

### Frontend
- [x] **API Client**: Added `getSystemConfig` and `updateSystemConfig` to `lib/api/settings.ts`.
- [x] **UI Refactor**:
    - Created **Image Processing** Section (Sliders, Switches).
    - Created **OCR Settings** Section (Model Priority List).
    - Created **System Info** Section.
- [x] **Feedback**: Added Toast notifications.

---

# Phase 24: OCR Prompt Structure Editor (RESOLVED)

## Goal
Enable advanced configuration of the OCR Prompt Structure directly from the Settings UI. This allows the user to fine-tune the JSON schema (keys and descriptions) sent to the AI model without touching code or raw JSON files.

## UI Design (`KeyValueEditor`)
To mimic the "n8n property input" experience:
- **Component**: `KeyValueList`
- **Rows**: Each key-value pair is a row.
- **Inputs**: Field Name (Key) and Description (Value).
- **Actions**: Delete button, Add Item button.
- **Grouping**: Tabs for `Document Info`, `Supplier`, `Receiver`, etc.

## Changes Implemented

### Frontend
- [x] **[NEW] Component `KeyValueList.tsx`**: Reusable component for editing dictionary data.
- [x] **Update `SettingsPage`**:
    - Added "OCR Prompt Configuration" section.
    - Implemented Tabs for sectioning.
    - Wired up `KeyValueList` to update the local `SystemConfig` state.

## Verification
1. **Persistence**: Changes to Image Processing and OCR Settings update `system_config.json`.
2. **Dynamic Prompting**: Changes to "Field Names" in the editor are saved and will be reflected in future OCR requests (as the backend reads this config).
3. **UX**: "Live" feedback, loading states, and toast notifications working.
