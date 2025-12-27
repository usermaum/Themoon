import { test, expect } from '@playwright/test';

test.describe('Roasting Flow', () => {
    test('should complete a single-origin roasting flow', async ({ page }) => {
        // 1. Navigate to Roasting Page
        await page.goto('/roasting');
        await expect(page).toHaveTitle(/The Moon Drip Bar/);

        // 2. Click "Start Roasting" on Single Origin card
        await page.getByRole('link', { name: 'Single Origin' }).click();
        await expect(page).toHaveURL(/\/roasting\/single-origin/);

        // 3. Select a Green Bean
        // Note: The select uses Radix UI, so we need to click the trigger and then the item
        await page.getByRole('combobox').click();
        // Wait for the list and select the first available item (e.g., Kenya)
        // We'll use a more generic approach: select any item from the list
        await page.getByRole('option').first().click();

        // 4. Enter Target Weight
        const targetInput = page.getByPlaceholder('0.0');
        await targetInput.fill('1.0');

        // 5. Enter Actual Output Weight
        // This input appears after simulation (calculated)
        const actualOutputInput = page.getByPlaceholder('0.00');
        await expect(actualOutputInput).toBeVisible();
        await actualOutputInput.fill('0.85');

        // 6. Click submit
        const submitBtn = page.getByRole('button', { name: '로스팅 실행' });
        await expect(submitBtn).toBeEnabled();
        await submitBtn.click();

        // 7. Handle Confirmation Dialog
        const confirmBtn = page.getByRole('button', { name: '확인' });
        await expect(confirmBtn).toBeVisible();
        await confirmBtn.click();

        // 8. Verify success message
        await expect(page.getByText('로스팅 완료!')).toBeVisible();
        await expect(page.getByText('최종 생산량')).toBeVisible();
        // The UI currently shows total stock quantity, verify it contains 'kg'
        await expect(page.getByText(/kg/).first()).toBeVisible();

        // 9. Click "새로운 로스팅 시작" to reset
        await page.getByRole('button', { name: '새로운 로스팅 시작' }).click();
        await expect(page.getByText('로스팅 완료!')).not.toBeVisible();
    });
    test('should complete a blend roasting flow', async ({ page }) => {
        // 1. Navigate to Blend Roasting Page
        await page.goto('/roasting/blend');

        // 2. Select a Blend Bean
        // Use text selector for the placeholder or value
        await page.getByText('블렌드를 선택하세요').click().catch(() => page.getByRole('combobox').click());
        // Wait for options and click the first valid option (ignoring the placeholder if it's an option)
        await page.getByRole('option').first().click();

        // 3. Enter Target Weight (placeholder "0")
        const targetInput = page.getByPlaceholder('0', { exact: true });
        await targetInput.fill('1.0');

        // 4. Enter Actual Output Weight (placeholder "0.0")
        const actualOutputInput = page.getByPlaceholder('0.0', { exact: true });
        await expect(actualOutputInput).toBeVisible();
        await actualOutputInput.fill('0.85');

        // 5. Click submit (Text contains "로스팅 실행")
        // Wait for button to be enabled (it depends on simulation)
        const submitBtn = page.getByRole('button', { name: /로스팅 실행/ });
        await expect(submitBtn).toBeEnabled({ timeout: 5000 });
        await submitBtn.click();

        // 6. Handle Confirmation Dialog
        const confirmBtn = page.getByRole('button', { name: '확인' });
        await expect(confirmBtn).toBeVisible();
        await confirmBtn.click();

        // 7. Verify success message
        await expect(page.getByText('블렌드 로스팅이 성공적으로 기록되었습니다.')).toBeVisible();
    });

    test('should show error when stock is insufficient', async ({ page }) => {
        // 1. Navigate to Roasting Page
        await page.goto('/roasting/single-origin');

        // 2. Select a Green Bean
        await page.getByRole('combobox').click();
        await page.getByRole('option').first().click();

        // 3. Enter Excessive Target Weight (e.g. 100000kg)
        const targetInput = page.getByPlaceholder('0.0');
        await targetInput.fill('100000.0');

        // 4. Enter Output Weight
        const actualOutputInput = page.getByPlaceholder('0.00');
        await actualOutputInput.fill('90000.0');

        // 5. Click submit
        const submitBtn = page.getByRole('button', { name: /로스팅 실행/ });
        await submitBtn.click();

        // 6. Verify Error Message
        // Check for specific shortage text pattern
        await expect(page.getByText(/재고가 부족하여/)).toBeVisible();
    });
});
