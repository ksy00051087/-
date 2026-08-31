// ===== SSAFY 이북 PDF 다운로드 스크립트 =====
// 사용법: 이북 페이지(예: .../ebook/unzip/xxxx/index.html)를 열어놓은 상태에서
// F12 → Console 탭 → 이 코드 전체 복사해서 붙여넣고 Enter

(async function () {
  try {
    const BASE = location.href.slice(0, location.href.lastIndexOf('/') + 1);
    console.log('[SSAFY→PDF] 시작:', BASE);

    // 1. project.json에서 페이지 목록 가져오기
    const projRes = await fetch(BASE + 'project.json');
    if (!projRes.ok) throw new Error('project.json을 찾을 수 없습니다. 이북 뷰어 페이지가 맞는지 확인하세요.');
    const proj = await projRes.json();
    const title = (proj.title || 'ssafy-ebook').replace(/[\\/:*?"<>|]/g, '_');
    const pageUrls = proj.pages.map((p) => BASE + p.background.url.replace('{ASSETS_DIR}', 'assets/'));
    console.log(`[SSAFY→PDF] 총 ${pageUrls.length}페이지 확인됨:`, title);

    // 2. jsPDF 라이브러리 로드 (eval 방식 - CSP script-src 제한 우회)
    if (!window.jspdf) {
      const libRes = await fetch('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
      const libCode = await libRes.text();
      const savedDefine = window.define;
      window.define = undefined; // AMD 경로 대신 전역(window.jspdf)에 붙도록 강제
      (0, eval)(libCode);
      window.define = savedDefine;
    }
    if (!window.jspdf) throw new Error('jsPDF 라이브러리를 불러오지 못했습니다.');
    const { jsPDF } = window.jspdf;
    console.log('[SSAFY→PDF] jsPDF 로드 완료');

    // 3. 이미지 fetch 유틸
    async function fetchAsDataURL(url) {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`이미지 다운로드 실패 (${res.status}): ${url}`);
      const blob = await res.blob();
      return await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    }
    function getImageSize(dataUrl) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve({ w: img.naturalWidth, h: img.naturalHeight });
        img.onerror = reject;
        img.src = dataUrl;
      });
    }

    // 4. 페이지별로 이미지 받아서 PDF에 추가
    let pdf = null;
    for (let i = 0; i < pageUrls.length; i++) {
      const dataUrl = await fetchAsDataURL(pageUrls[i]);
      const { w, h } = await getImageSize(dataUrl);
      const orientation = w > h ? 'l' : 'p';
      if (!pdf) {
        pdf = new jsPDF({ orientation, unit: 'px', format: [w, h], compress: true });
      } else {
        pdf.addPage([w, h], orientation);
      }
      pdf.addImage(dataUrl, 'JPEG', 0, 0, w, h);
      console.log(`[SSAFY→PDF] 진행률: ${i + 1}/${pageUrls.length}`);
    }

    // 5. 다운로드
    pdf.save(`${title}.pdf`);
    console.log('[SSAFY→PDF] ✅ 완료! 다운로드 폴더를 확인하세요:', `${title}.pdf`);
  } catch (err) {
    console.error('[SSAFY→PDF] ❌ 실패:', err);
    alert('PDF 생성 실패: ' + err.message);
  }
})();
