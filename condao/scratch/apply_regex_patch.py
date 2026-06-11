import os
import re

files = ['dalat.html', 'vinhhy.html', 'vungtau.html']

old_pos = """            clone.style.position = 'fixed';
            clone.style.left = '-20000px';"""

new_pos = """            clone.style.position = 'absolute';
            clone.style.left = '0px';
            clone.style.top = '0px';
            clone.style.zIndex = '-9999';"""

new_doc = """            html2canvas(clone, { scale: 2, useCORS: true }).then(canvas => {
                const imgData = canvas.toDataURL('image/jpeg', 1.0);
                const pdfWidth = doc.internal.pageSize.getWidth();
                const pdfHeight = doc.internal.pageSize.getHeight();
                
                const imgWidth = pdfWidth - 40; // 20pt margin on each side
                const imgHeight = (canvas.height * imgWidth) / canvas.width;

                let heightLeft = imgHeight;
                let position = 20;

                doc.addImage(imgData, 'JPEG', 20, position, imgWidth, imgHeight);
                heightLeft -= (pdfHeight - 40);

                while (heightLeft > 0) {
                    position = heightLeft - imgHeight + 20;
                    doc.addPage();
                    doc.addImage(imgData, 'JPEG', 20, position, imgWidth, imgHeight);
                    heightLeft -= (pdfHeight - 40);
                }

                doc.save(filename);
                setTimeout(() => { try { document.body.removeChild(clone); } catch (e) {} }, 100);
            }).catch(err => {
                console.error('html2canvas error:', err);
                document.body.removeChild(clone);
                exportItinerary_Fallback(doc, filename);
            });"""

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # replace position
    content = content.replace(old_pos, new_pos)
    
    # replace doc.html block using regex
    pattern = re.compile(r'            doc\.html\(clone, \{.*?\n            \}\);', re.DOTALL)
    content = pattern.sub(new_doc, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
