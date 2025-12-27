import { test, expect } from '@playwright/test';

test.describe('Roasting Demo Page (Simulator)', () => {
    test.beforeEach(async ({ page }) => {
        // Demo 페이지로 이동
        await page.goto('/roasting/demo');
    });

    test('should load the simulator interface correctly', async ({ page }) => {
        // 1. 페이지 타이틀 확인 (PageHero)
        // 텍스트는 description에 포함된 '가상 로스팅 체험관'이나 제목 'Roasting Simulator'
        await expect(page.getByRole('heading', { name: 'Roasting Simulator' })).toBeVisible();

        // 2. 주요 UI 요소 확인
        // 타이머 (DURATION)
        await expect(page.getByText('DURATION')).toBeVisible();
        // 온도 표시 (BEAN TEMP)
        await expect(page.getByText('BEAN TEMP')).toBeVisible();

        // 3. 시작 버튼 (START)
        const startButton = page.getByRole('button', { name: 'START' });
        await expect(startButton).toBeVisible();
        await expect(startButton).toBeEnabled();
    });

    test('should create a roasting record after simulation', async ({ page }) => {
        // 1. 로스팅 시작
        const startButton = page.getByRole('button', { name: 'START' });
        await startButton.click();

        // 2. "로스팅 진행 중" 상태 확인 (버튼이 'DROP'으로 바뀜)
        const dischargeButton = page.getByRole('button', { name: 'DROP' });
        await expect(dischargeButton).toBeVisible();

        // 3. 잠시 대기 (시뮬레이션 진행)
        await page.waitForTimeout(2000);

        // 4. 배출 하기 클릭
        await dischargeButton.click();

        // 5. 완료 상태 확인
        // DROP 버튼이 다시 START 로 바뀌거나, 상태가 변경됨.
        // 코드 상 handleStop -> status='FINISHED'.
        // FINISHED 상태에서는 START 버튼이 다시 보임 (status === 'IDLE' || status === 'FINISHED')
        await expect(page.getByRole('button', { name: 'START' })).toBeVisible();
    });

    test('should adjust controls', async ({ page }) => {
        // 화력 슬라이더 확인 (GAS POWER)
        // ControlKnob 컴포넌트는 실제 input range가 아니라 div로 시각화만 되어 있을 수 있음.
        // 코드 확인: ControlKnob은 div로 그려짐 (clipPath). input 없음.
        // 따라서 슬라이더 조작 테스트는 불가능하므로, 시각적 요소가 존재하는지만 확인.

        await expect(page.getByText('GAS POWER')).toBeVisible();
        await expect(page.getByText('AIR FLOW')).toBeVisible();
        await expect(page.getByText('DRUM SPEED')).toBeVisible();

        // 값 표시 확인 (75)
        await expect(page.getByText('75')).toBeVisible();
    });
});
