'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { BlendAPI, Bean, BeanAPI, Blend, BlendRecipeItem } from '@/lib/api';
import PageHero from '@/components/ui/page-hero';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Trash2, Layers, Save, ArrowLeft, Plus } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

// 블렌드 상세 및 수정 페이지
export default function BlendDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const blendId = parseInt(params.id);

  // 상태 관리
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [blend, setBlend] = useState<Blend | null>(null);
  const [availableBeans, setAvailableBeans] = useState<Bean[]>([]);

  // 폼 상태
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [targetRoastLevel, setTargetRoastLevel] = useState('');
  const [notes, setNotes] = useState('');
  const [recipeItems, setRecipeItems] = useState<{ beanId: string; percent: string }[]>([]);

  // Dialog State
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogConfig, setDialogConfig] = useState({ title: '', message: '', onConfirm: () => {} });

  const showDialog = (title: string, message: string, onConfirm?: () => void) => {
    setDialogConfig({
      title,
      message,
      onConfirm: onConfirm || (() => {}),
    });
    setDialogOpen(true);
  };

  // 초기 데이터 로드
  useEffect(() => {
    const fetchData = async () => {
      try {
        // 원두 목록 로드 (생두만)
        const beansData = await BeanAPI.getAll({ limit: 100, type: ['GREEN_BEAN'] });
        // 블렌드 정보 로드
        const blendData = await BlendAPI.getOne(blendId);

        // BeanListResponse { items: Bean[], ... }
        setAvailableBeans(beansData.items);

        setBlend(blendData);

        // 폼 초기화
        setName(blendData.name);
        setDescription(blendData.description || '');
        setTargetRoastLevel(blendData.target_roast_level || '');
        setNotes(blendData.notes || '');

        // 레시피 초기화 (비율 0.4 -> 40%)
        const loadedRecipe = blendData.recipe.map((item) => ({
          beanId: item.bean_id.toString(),
          percent: (item.ratio * 100).toString(),
        }));
        setRecipeItems(loadedRecipe);
      } catch (err) {
        console.error('Failed to load blend data:', err);
        showDialog('오류', '블렌드 정보를 불러올 수 없습니다.', () => router.push('/blends'));
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [blendId, router]);

  const totalPercent = recipeItems.reduce((sum, item) => sum + (parseFloat(item.percent) || 0), 0);

  // 핸들러 함수들
  const addRecipeItem = () => {
    setRecipeItems([...recipeItems, { beanId: '', percent: '' }]);
  };

  const removeRecipeItem = (index: number) => {
    if (recipeItems.length <= 1) {
      showDialog('알림', '최소 하나의 원두는 포함되어야 합니다.');
      return;
    }
    const newItems = [...recipeItems];
    newItems.splice(index, 1);
    setRecipeItems(newItems);
  };

  const updateRecipeItem = (index: number, field: 'beanId' | 'percent', value: string) => {
    const newItems = [...recipeItems];
    newItems[index] = { ...newItems[index], [field]: value };
    setRecipeItems(newItems);
  };

  const handleDelete = async () => {
    if (!confirm('정말로 이 블렌드를 삭제하시겠습니까?')) return;

    try {
      await BlendAPI.delete(blendId);
      showDialog('삭제 완료', '블렌드가 삭제되었습니다.', () => router.push('/blends'));
    } catch (err) {
      showDialog('오류', '삭제에 실패했습니다.');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (Math.abs(totalPercent - 100) > 0.1) {
      showDialog('비율 오류', `비율의 합은 100%여야 합니다. (현재: ${totalPercent}%)`);
      return;
    }

    try {
      setSubmitting(true);

      // 유효한 레시피 항목만 필터링 (빈 값 제외)
      const validItems = recipeItems.filter((item) => item.beanId && !isNaN(parseInt(item.beanId)));

      if (validItems.length === 0) {
        alert('최소 하나 이상의 유효한 원두가 포함되어야 합니다.');
        setSubmitting(false);
        return;
      }

      const recipe: BlendRecipeItem[] = validItems.map((item) => ({
        bean_id: parseInt(item.beanId),
        ratio: parseFloat(item.percent) / 100.0,
      }));

      await BlendAPI.update(blendId, {
        name,
        description,
        target_roast_level: targetRoastLevel,
        notes,
        recipe,
      });

      showDialog('수정 완료', '블렌드 수정사항이 저장되었습니다.', () => {
        router.push('/blends');
      });
    } catch (err) {
      console.error('Failed to update blend:', err);
      showDialog('오류', '수정에 실패했습니다.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-latte-600">Loading blend details...</div>;
  }

  return (
    <div className="min-h-screen">
      <PageHero
        title="Edit Blend Recipe"
        description={`'${blend?.name}' 레시피를 수정합니다.`}
        icon={<Layers />}
        image="/images/hero/beans-hero.png"
        className="mb-8"
      />

      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="flex justify-between items-center mb-6">
          <Button
            variant="ghost"
            onClick={() => router.back()}
            className="pl-0 hover:bg-transparent hover:text-latte-800"
          >
            <ArrowLeft className="w-4 h-4 mr-2" /> 목록으로 돌아가기
          </Button>
          <Button
            variant="destructive"
            onClick={handleDelete}
            className="bg-red-50 text-red-600 hover:bg-red-100 hover:text-red-700 border-none"
          >
            <Trash2 className="w-4 h-4 mr-2" /> 블렌드 삭제
          </Button>
        </div>

        <Card className="border-latte-200 shadow-lg">
          <CardContent className="p-8">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* 기본 정보 */}
              <div className="space-y-4">
                <h3 className="text-lg font-serif font-bold text-latte-800 border-b border-latte-100 pb-2">
                  기본 정보
                </h3>
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <label className="text-sm font-medium text-latte-600">블렌드 이름 *</label>
                    <Input
                      required
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="bg-latte-50/50"
                    />
                  </div>
                  <div className="grid gap-2">
                    <label className="text-sm font-medium text-latte-600">설명</label>
                    <Input
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                      className="bg-latte-50/50"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="grid gap-2">
                      <label className="text-sm font-medium text-latte-600">
                        목표 로스팅 포인트
                      </label>
                      <Input
                        value={targetRoastLevel}
                        onChange={(e) => setTargetRoastLevel(e.target.value)}
                        className="bg-latte-50/50"
                      />
                    </div>
                    <div className="grid gap-2">
                      <label className="text-sm font-medium text-latte-600">참고 노트</label>
                      <Input
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                        className="bg-latte-50/50"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* 레시피 구성 */}
              <div className="space-y-4">
                <div className="flex justify-between items-end border-b border-latte-100 pb-2">
                  <h3 className="text-lg font-serif font-bold text-latte-800">레시피 구성</h3>
                  <span
                    className={`text-sm font-bold ${totalPercent === 100 ? 'text-green-600' : 'text-red-500'}`}
                  >
                    총 합계: {totalPercent}%
                  </span>
                </div>

                <div className="space-y-3">
                  {recipeItems.map((item, index) => (
                    <div
                      key={index}
                      className="flex gap-3 items-end p-4 bg-latte-50 rounded-xl relative group"
                    >
                      <div className="flex-1">
                        <label className="text-xs text-latte-500 mb-1 block">원두 선택</label>
                        <Select
                          value={item.beanId}
                          onValueChange={(value) => updateRecipeItem(index, 'beanId', value)}
                        >
                          <SelectTrigger className="w-full h-10 bg-white">
                            <SelectValue placeholder="원두를 선택하세요" />
                          </SelectTrigger>
                          <SelectContent>
                            {availableBeans.map((bean) => (
                              <SelectItem key={bean.id} value={String(bean.id)}>
                                {bean.name}{' '}
                                <span className="text-latte-400 text-xs ml-1">({bean.origin})</span>
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="w-24">
                        <label className="text-xs text-latte-500 mb-1 block">비율 (%)</label>
                        <div className="relative">
                          <Input
                            type="number"
                            value={item.percent}
                            onChange={(e) => updateRecipeItem(index, 'percent', e.target.value)}
                            className="pr-6 bg-white"
                            min="0"
                            max="100"
                            required
                          />
                          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-latte-400">
                            %
                          </span>
                        </div>
                      </div>
                      <Button
                        type="button"
                        variant="destructive"
                        size="icon"
                        onClick={() => removeRecipeItem(index)}
                        className="mb-[1px]"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}

                  <Button
                    type="button"
                    variant="outline"
                    className="w-full border-dashed border-2 border-latte-200 text-latte-500 hover:border-latte-400 hover:text-latte-700 hover:bg-latte-50"
                    onClick={addRecipeItem}
                  >
                    <Plus className="w-4 h-4 mr-2" /> 원두 추가하기
                  </Button>
                </div>
              </div>

              <div className="pt-6 border-t border-latte-100 flex justify-end gap-3">
                <Button type="button" variant="ghost" onClick={() => router.back()}>
                  취소
                </Button>
                <Button
                  type="submit"
                  className="bg-latte-800 hover:bg-latte-900 text-white min-w-[120px]"
                  disabled={submitting}
                >
                  {submitting ? (
                    '저장 중...'
                  ) : (
                    <>
                      <Save className="w-4 h-4 mr-2" /> 수정사항 저장
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
      {/* 알림 대화상자 */}
      <AlertDialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{dialogConfig.title}</AlertDialogTitle>
            <AlertDialogDescription>{dialogConfig.message}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogAction
              onClick={() => {
                setDialogOpen(false);
                dialogConfig.onConfirm();
              }}
            >
              확인
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
