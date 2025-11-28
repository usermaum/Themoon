const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, LevelFormat, TableOfContents, PageBreak } = require('docx');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

const doc = new Document({
  styles: {
    default: { document: { run: { font: "맑은 고딕", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "2C5282", font: "맑은 고딕" },
        paragraph: { spacing: { before: 240, after: 360 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, color: "1a365d", font: "맑은 고딕" },
        paragraph: { spacing: { before: 480, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "2c5282", font: "맑은 고딕" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, color: "4299e1", font: "맑은 고딕" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 } }
    ]
  },
  numbering: {
    config: [
      { reference: "bullet-list",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      // 표지
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("더문(The Moon)")] }),
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("로스팅 및 재고 관리")] }),
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("운영 계획안")] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 480 },
        children: [new TextRun({ text: "v1.0", size: 24, color: "718096" })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // 목차
      new TableOfContents("목차", { hyperlink: true, headingStyleRange: "1-3" }),

      new Paragraph({ children: [new PageBreak()] }),

      // 1. 개요
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. 개요")] }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 문서는 '더문(The Moon)'의 효율적인 로스팅 생산 관리 및 재고 운영을 위한 기준 정보와 업무 시나리오를 정의합니다. 원두의 입고부터 로스팅, 블렌딩, 그리고 최종 제품 생산에 이르는 프로세스를 체계화하여 데이터 기반의 운영을 목표로 합니다.")]
      }),

      // 1.1 용어 정의
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.1 용어 정의")] }),

      new Paragraph({
        spacing: { before: 120, after: 60 },
        children: [new TextRun({ text: "재료 및 제품 분류", bold: true, size: 24 })]
      }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "생두 (Green Bean): ", bold: true }), new TextRun("로스팅 전의 커피 원두 (입고된 원재료)")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "원두 (Roasted Bean): ", bold: true }), new TextRun("로스팅 후의 커피 원두")
      ]}),
      new Paragraph({
        indent: { left: 720 },
        spacing: { before: 60 },
        children: [new TextRun("- 싱글 오리진 원두: 한 종류의 생두만 로스팅한 원두")]
      }),
      new Paragraph({
        indent: { left: 720 },
        children: [new TextRun("- 블렌드 원두: 여러 종류의 생두를 배합하여 함께 로스팅한 원두")]
      }),

      new Paragraph({
        spacing: { before: 240, after: 60 },
        children: [new TextRun({ text: "로스팅 프로필", bold: true, size: 24 })]
      }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "신콩 (Light Roast): ", bold: true }), new TextRun("밝은 로스팅 (약볶음) - 산미와 풍미 강조")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "탄콩 (Dark Roast): ", bold: true }), new TextRun("깊은 로스팅 (강볶음) - 바디감과 쓴맛 강조")
      ]}),

      new Paragraph({ children: [new PageBreak()] }),

      // 2. 원두 마스터 데이터
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. 원두 마스터 데이터")] }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("현재 취급 중인 생두와 로스팅 결과물인 싱글 오리진 원두의 목록입니다.")]
      }),

      // 원두 리스트 테이블
      new Table({
        columnWidths: [600, 1800, 3300, 800, 2860],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders, width: { size: 600, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "No", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 1800, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "한글명", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 3300, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "영문 표기 (명세서 기준)", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 800, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "국가", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 2860, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "상세 정보", bold: true, color: "FFFFFF", size: 20 })] })]
              })
            ]
          }),
          ...createBeanRows([
            ["1", "예가체프", "Ethiopia G2 Yirgacheffe Washed", "Eth", "수세식, G2등급"],
            ["2", "모모라", "Ethiopia G1 Danse Mormora Natural", "Eth", "구지 지역, 내추럴, G1등급"],
            ["3", "코케허니", "Ethiopia G1 Yirgacheffe Koke Honey Natural", "Eth", "예가체프, 허니 프로세스"],
            ["4", "우라가", "Ethiopia G1 Guji Uraga Washed", "Eth", "구지 우라가, 수세식"],
            ["5", "마사이", "Kenya AA FAQ", "K", "AA등급, FAQ 품질"],
            ["6", "키린야가", "Kenya PB TOP Kirinyaga", "K", "피베리, 키린야가 지역"],
            ["7", "후일라", "Colombia Supremo Huila", "Co", "수프리모 등급"],
            ["8", "안티구아", "Guatemala SHB Antigua", "Gu", "SHB(Strictly Hard Bean)"],
            ["9", "엘탄케", "Costa Rica El Tanque", "Cos", "엘탄케 농장"],
            ["10", "파젠다 카르모", "Brazil Fazenda Carmo Estate Natural", "Br", "SC16UP, 내추럴"],
            ["11", "디카페 SDM", "Ethiopia Decaf (SDM)", "Eth", "디카페인 (공법 미상)"],
            ["12", "디카페 SM", "Colombia Supremo Popayan Sugarcane Decaf", "Co", "슈가케인 디카페인"],
            ["13", "스위스워터", "Brazil Swiss Water Decaf", "Br", "스위스워터 공법"],
            ["14", "시다모 G4", "Ethiopia G4 Sidamo Natural", "Eth", "블렌딩용, G4등급"],
            ["15", "산토스", "Brazil NY2 FC Santos", "Br", "블렌딩용, NY2등급"]
          ])
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // 3. 블렌딩 레시피
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. 블렌딩 레시피")] }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("더문의 시그니처 블렌드 제품 생산을 위한 표준 배합비입니다.")]
      }),

      // 3.1 풀문
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.1 풀문 (Full Moon)")] }),
      new Table({
        columnWidths: [3120, 6240],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          createInfoRow("제품 설명", "더문의 대표 하우스 블렌드"),
          createInfoRow("기준 판매가", "22,000원"),
          createInfoRow("기준 손실률", "15%"),
          createInfoRow("배합 비율", "AA FAQ (마사이): 40%\n안티구아: 40%\n모모라: 10%\n시다모 G4: 10%")
        ]
      }),

      new Paragraph({ spacing: { before: 360 } }),

      // 3.2 뉴문
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.2 뉴문 (New Moon)")] }),
      new Table({
        columnWidths: [3120, 6240],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          createInfoRow("제품 설명", "대중적인 맛을 지향하는 블렌드"),
          createInfoRow("기준 손실률", "15%"),
          createInfoRow("배합 비율", "산토스 (브라질): 60%\n후일라 (콜롬비아): 30%\n시다모 G4: 10%")
        ]
      }),

      new Paragraph({ spacing: { before: 360 } }),

      // 3.3 이클립스문
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.3 이클립스문 (Eclipse Moon)")] }),
      new Table({
        columnWidths: [3120, 6240],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          createInfoRow("제품 설명", "디카페인 블렌드"),
          createInfoRow("기준 손실률", "15%"),
          createInfoRow("배합 비율", "디카페 SM (콜롬비아): 60%\n스위스워터 (브라질): 40%")
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // 4. 운영 시나리오
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. 운영 시나리오")] }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("실제 매장 운영 시 발생하는 주요 업무 흐름을 정의합니다.")]
      }),

      // 4.1 자재 입고
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("4.1 자재 입고 (Material Inbound)")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun("외부 업체로부터 생두를 구매하고, 거래 명세서를 기반으로 입고를 처리하는 단계입니다.")]
      }),

      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "문서 확보: ", bold: true }), new TextRun("거래처로부터 받은 견적서 또는 영수증 준비")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "입고 등록 (OCR): ", bold: true }), new TextRun("시스템에 문서 업로드 및 자동 인식")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "데이터 검증: ", bold: true }), new TextRun("추출된 데이터와 실제 입고 물품 일치 확인")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "입고 확정: ", bold: true }), new TextRun("생두 재고 증가 및 매입 단가 반영")
      ]}),

      new Paragraph({ spacing: { before: 360 } }),

      // 4.2 싱글 오리진 로스팅
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("4.2 싱글 오리진 로스팅")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun("한 종류의 생두를 볶아 싱글 오리진 원두로 가공하는 단계입니다.")]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("작업 준비")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun("로스팅할 생두 품목 선택 (예: 예가체프 생두)")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun("로스팅 프로필 선택: 신콩 또는 탄콩")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun("목표 원두 생산량(kg) 입력")
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("생두 투입량 자동 계산")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun("시스템은 목표 생산량과 평균 손실률을 기반으로 필요한 생두량을 자동 계산합니다.")]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 120 },
        shading: { fill: "EDF2F7", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "필요 생두량 = 목표 원두 생산량 / (1 - 손실률)", bold: true, color: "2D3748" })]
      }),
      new Paragraph({
        spacing: { before: 120, after: 60 },
        children: [new TextRun({ text: "예시:", bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun("목표: 예가체프-신콩 원두 10kg 생산")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun("평균 손실률: 15%")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "필요 생두량: 11.76kg", bold: true, color: "2C5282" })
      ]}),

      new Paragraph({ children: [new PageBreak()] }),

      // 5. 명세서 입고 데이터 (요약)
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("5. 명세서 입고 데이터")] }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("실제 거래 명세서를 기반으로 분석한 입고 내역입니다. (총 11건)")]
      }),

      // 명세서 요약 테이블
      new Table({
        columnWidths: [1400, 2100, 2400, 1800, 1660],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders, width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "명세서 번호", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 2100, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "작성 일자", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 2400, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "공급자", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 1800, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "합계 금액", bold: true, color: "FFFFFF", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders, width: { size: 1660, type: WidthType.DXA },
                shading: { fill: "4299e1", type: ShadingType.CLEAR },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "총 중량", bold: true, color: "FFFFFF", size: 20 })] })]
              })
            ]
          }),
          ...createInvoiceRows([
            ["1650.PNG", "2025-10-29", "지에스씨인터내셔날", "1,845,000원", "120kg"],
            ["1651.PNG", "2025-09-26", "지에스씨인터내셔날", "3,058,000원", "140kg"],
            ["1652.PNG", "2025-09-03", "지에스씨인터내셔날", "1,536,000원", "120kg"],
            ["1653.PNG", "2025-07-31", "지에스씨인터내셔날", "2,198,000원", "140kg"],
            ["1654.PNG", "2025-07-08", "지에스씨인터내셔날", "486,000원", "30kg"],
            ["1655.PNG", "2025-05-27", "지에스씨인터내셔날", "2,797,000원", "161kg"],
            ["1656.PNG", "2025-03-27", "지에스씨인터내셔날", "882,000원", "60kg"],
            ["1657.PNG", "2025-03-11", "지에스씨인터내셔날", "3,752,000원", "280kg"],
            ["1658.PNG", "2025-02-17", "지에스씨인터내셔날", "1,060,000원", "80kg"],
            ["1659.PNG", "2024-12-24", "지에스씨인터내셔날", "2,542,000원", "200kg"],
            ["1660.JPG", "2025-11-08", "아실로(온라인)", "494,000원", "40kg"]
          ])
        ]
      }),

      new Paragraph({
        spacing: { before: 360, after: 120 },
        children: [new TextRun({ text: "총 입고 내역 요약", bold: true, size: 24, color: "2C5282" })]
      }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "총 거래 건수: ", bold: true }), new TextRun("11건")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "총 구매 금액: ", bold: true }), new TextRun("20,650,000원")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "총 입고 중량: ", bold: true }), new TextRun("1,371kg")
      ]}),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [
        new TextRun({ text: "기간: ", bold: true }), new TextRun("2024-12-24 ~ 2025-11-08")
      ]}),

      // 마지막 페이지
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 1440 },
        children: [new TextRun({ text: "문서 끝", size: 28, color: "718096" })]
      })
    ]
  }]
});

// Helper function: Bean table rows
function createBeanRows(data) {
  return data.map((row, idx) => {
    const isEven = idx % 2 === 0;
    return new TableRow({
      children: [
        new TableCell({
          borders: cellBorders, width: { size: 600, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun(row[0])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 1800, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun(row[1])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 3300, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun(row[2])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 800, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun(row[3])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 2860, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun(row[4])] })]
        })
      ]
    });
  });
}

// Helper function: Info row (2-column)
function createInfoRow(label, value) {
  return new TableRow({
    children: [
      new TableCell({
        borders: cellBorders, width: { size: 3120, type: WidthType.DXA },
        shading: { fill: "EDF2F7", type: ShadingType.CLEAR },
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({ children: [new TextRun({ text: label, bold: true })] })]
      }),
      new TableCell({
        borders: cellBorders, width: { size: 6240, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: value.split('\n').map(line =>
          new Paragraph({ children: [new TextRun(line)] })
        )
      })
    ]
  });
}

// Helper function: Invoice rows
function createInvoiceRows(data) {
  return data.map((row, idx) => {
    const isEven = idx % 2 === 0;
    return new TableRow({
      children: [
        new TableCell({
          borders: cellBorders, width: { size: 1400, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun(row[0])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 2100, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun(row[1])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 2400, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun(row[2])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 1800, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun(row[3])] })]
        }),
        new TableCell({
          borders: cellBorders, width: { size: 1660, type: WidthType.DXA },
          shading: { fill: isEven ? "FFFFFF" : "F7FAFC", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun(row[4])] })]
        })
      ]
    });
  });
}

// Save document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/mnt/d/Ai/WslProject/TheMoon/Documents/Planning/더문_로스팅_운영계획안.docx", buffer);
  console.log("Word 문서가 성공적으로 생성되었습니다!");
});
