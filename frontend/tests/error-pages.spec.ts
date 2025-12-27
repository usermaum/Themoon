import { test, expect } from '@playwright/test';

test.describe('Error Pages (Mascot Theme)', () => {

    test('should display 404 page with Mascot for non-existent routes', async ({ page }) => {
        // 1. Navigate to a random non-existent page
        await page.goto('/non-existent-page-random-123');

        // 2. Verify Title and Description
        // "Page Not Found" or "페이지를 찾을 수 없습니다"
        // Using loose matching or specific text from the actual implementation
        await expect(page.getByRole('heading', { level: 2 })).toContainText(/Page Not Found|페이지를 찾을 수 없습니다/i);

        // 3. Verify Mascot presence (Video element)
        // Waif for animation (Framer Motion opacity: 0 -> 1)
        const mascotVideo = page.locator('video').first();
        await expect(mascotVideo).toBeVisible({ timeout: 10000 });

        // Optional: Check if source is correct
        // Note: src might be full URL, so use toContain
        const videoSource = mascotVideo.locator('source');
        await expect(videoSource).toHaveAttribute('src', /\/videos\/mascot_not_found.mp4/);

        // 4. Verify "Go Home" button
        const homeButton = page.getByRole('button', { name: /Home|홈으로/i });
        await expect(homeButton).toBeVisible();

        // 5. Click Home and verify navigation to /
        await homeButton.click();
        await expect(page).toHaveURL(/\/$/);
    });

});
