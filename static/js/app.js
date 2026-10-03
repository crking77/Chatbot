(function(){
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
function toast(msg,type){let box=$('#toasts');if(!box)return;const t=document.createElement('div');t.className='toast '+(type||'');t.textContent=msg;box.appendChild(t);setTimeout(()=>t.remove(),3800)}
function busy(btn,on,label){if(!btn)return;if(on){btn.dataset.t=btn.innerHTML;btn.disabled=true;btn.innerHTML='<span class="spin"></span>'+(label||'Đang xử lý...')}else{btn.disabled=false;btn.innerHTML=btn.dataset.t||btn.innerHTML}}
// Xác nhận trước khi xóa
$$('a[data-confirm]').forEach(a=>a.addEventListener('click',e=>{if(!confirm(a.dataset.confirm))e.preventDefault()}));
// Nút/biểu mẫu chạy lâu (tạo chỉ mục): hiện trạng thái đang xử lý
$$('form[data-loading]').forEach(f=>f.addEventListener('submit',()=>busy($('button[type=submit]',f),true,f.dataset.loading)));
// Hiện/ẩn mật khẩu
$$('[data-toggle-pw]').forEach(b=>b.addEventListener('click',()=>{const i=$('input',b.parentElement);i.type=i.type==='password'?'text':'password';b.textContent=i.type==='password'?'Hiện':'Ẩn'}));
// Thêm FAQ không tải lại trang
const add=$('#addForm');
if(add)add.addEventListener('submit',async e=>{e.preventDefault();const btn=$('button[type=submit]',add);busy(btn,true,'Đang lưu...');
 try{const r=await fetch(add.action,{method:'POST',body:new FormData(add)});
  if(r.ok){toast('Đã thêm FAQ mới. Nhớ tạo lại chỉ mục để chatbot dùng được.','ok');add.reset();$('input',add).focus()}
  else{let m='Không thêm được (mã '+r.status+')';try{const j=await r.json();if(j.error)m=j.error==='Question and answer are required'?'Vui lòng nhập đủ câu hỏi và câu trả lời':j.error}catch(_){}toast(m,'err')}
 }catch(_){toast('Mất kết nối tới máy chủ','err')}busy(btn,false)});
// Khung thử chatbot
const ask=$('#askForm'),chat=$('#chat');
function bubble(t,c){const d=document.createElement('div');d.className='b '+c;d.textContent=t;const em=$('.empty',chat);if(em)em.remove();chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
if(ask)ask.addEventListener('submit',async e=>{e.preventDefault();const inp=$('input[name=question]',ask),q=inp.value.trim();if(!q)return;
 bubble(q,'me');inp.value='';const btn=$('button[type=submit]',ask);btn.disabled=true;const w=bubble('Đang tìm câu trả lời...','bot');
 try{const r=await fetch(ask.action+'?question='+encodeURIComponent(q));const j=await r.json();
  if(r.ok&&j.response){w.textContent=j.response}else{w.className='b err';w.textContent=j.error||('Lỗi máy chủ (mã '+r.status+')')}
 }catch(_){w.className='b err';w.textContent='Không nhận được phản hồi. Xem cửa sổ dòng lệnh của máy chủ để biết lỗi.'}
 btn.disabled=false;inp.focus();chat.scrollTop=chat.scrollHeight});
// Lọc danh sách FAQ
const f=$('#filter');
if(f)f.addEventListener('input',()=>{const k=f.value.trim().toLowerCase();let n=0;$$('#rows tr').forEach(tr=>{const ok=tr.textContent.toLowerCase().includes(k);tr.hidden=!ok;if(ok)n++});$('#shown').textContent=n;$('#none').hidden=n>0});
})();
