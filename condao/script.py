import re

files = ["vinhhy.html", "vungtau.html", "dalat.html"]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update loadPlanFromStorage
    content = re.sub(
        r'(function loadPlanFromStorage\(\) \{\n\s*const saved = localStorage\.getItem\([^)]+\);\n\s*if \(saved\) \{\n\s*try \{\n\s*customPlan = JSON\.parse\(saved\);)',
        r'\1\n            for (let i = 1; i <= 4; i++) {\n                if (customPlan[day]) {\n                    customPlan[day].sort((a, b) => parseTimeToMinutes(a.time) - parseTimeToMinutes(b.time));\n                }\n            }',
        content
    )
    
    # 2. Add parseTimeToMinutes and update sort in addCustomItineraryItem
    content = content.replace(
        'customPlan[day].sort((a, b) => a.time.localeCompare(b.time));',
        'customPlan[day].sort((a, b) => parseTimeToMinutes(a.time) - parseTimeToMinutes(b.time));'
    )
    
    if "function parseTimeToMinutes" not in content:
        content = content.replace(
            'function addCustomItineraryItem() {',
            'function parseTimeToMinutes(timeStr) {\n    if (!timeStr) return 0;\n    const match = timeStr.match(/(\\d{1,2})\\s*[:hH]\\s*(\\d{2})/);\n    if (match) {\n        return parseInt(match[1], 10) * 60 + parseInt(match[2], 10);\n    }\n    const hourMatch = timeStr.match(/(\\d{1,2})\\s*[hH]?/);\n    if (hourMatch) {\n        return parseInt(hourMatch[1], 10) * 60;\n    }\n    return 9999;\n}\n\nfunction addCustomItineraryItem() {'
        )
    
    # 3. Update exportItinerary pdf layout fixes
    pattern_export = r'(\s*let htmlRenderAttempted = false;\s*if \(presetView && typeof doc\.html === \'function\'\) \{[\s\S]*?\n\s*\})'
    replacement_export = r'''
    if (presetView) {
        try {
            const cloneWrapper = document.createElement('div');
            cloneWrapper.className = "bg-white p-8 md:p-12"; 
            cloneWrapper.style.width = '800px';
            cloneWrapper.style.position = 'absolute';
            cloneWrapper.style.left = '-9999px';
            cloneWrapper.style.top = '0px';

            const clone = presetView.cloneNode(true);
            clone.style.display = 'block';
            cloneWrapper.appendChild(clone);
            document.body.appendChild(cloneWrapper);

            const animatedEls = cloneWrapper.querySelectorAll('.timeline-item, .destination-card, .animate-fade-in-up, .animate-fade-in');
            animatedEls.forEach(el => {
                el.classList.add('visible');
                el.style.opacity = '1';
                el.style.transform = 'none';
                el.style.animation = 'none';
            });

            html2canvas(cloneWrapper, { 
                scale: 2, 
                useCORS: true,
                windowWidth: 800,
                logging: false
            }).then(canvas => {
                const imgData = canvas.toDataURL('image/jpeg', 1.0);
                const pdfWidth = doc.internal.pageSize.getWidth();
                const pdfHeight = doc.internal.pageSize.getHeight();
                
                const marginX = 20;
                const marginY = 20;
                const imgWidth = pdfWidth - marginX * 2;
                const pageHeight = pdfHeight - marginY * 2;
                const imgHeight = (canvas.height * imgWidth) / canvas.width;

                let heightLeft = imgHeight;
                let position = marginY;

                doc.addImage(imgData, 'JPEG', marginX, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;

                while (heightLeft > 0) {
                    position = position - pageHeight;
                    doc.addPage();
                    doc.addImage(imgData, 'JPEG', marginX, position, imgWidth, imgHeight);
                    
                    doc.setFillColor(255, 255, 255);
                    doc.rect(0, 0, pdfWidth, marginY, 'F');
                    doc.rect(0, pdfHeight - marginY, pdfWidth, marginY, 'F');
                    
                    heightLeft -= pageHeight;
                }

                doc.save(filename);
                setTimeout(() => { try { document.body.removeChild(cloneWrapper); } catch (e) {} }, 100);
            }).catch(err => {
                console.error('html2canvas error:', err);
                try { document.body.removeChild(cloneWrapper); } catch (e) {}
                exportItinerary_Fallback(doc, filename);
            });
            return;
        } catch (e) {
            console.error('HTML rendering failed, falling back to text:', e);
        }
    }
'''
    content = re.sub(pattern_export, replacement_export, content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated " + file)
