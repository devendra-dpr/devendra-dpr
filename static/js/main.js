

$(document).ready(() => {
    const form_ele = $('form')
    
    // Review Copy Alert
    const ReviewCopyAlert = document.querySelector('#myAlert')
    
    async function serverReq(url, method = "GET", headers = {}, body=null) {
        const resp = await fetch(url, { method, headers, body });
        if (resp.ok){
            return await resp.text()
        }
        else{
            alert('Your form was not sent successfully.'); 
            throw Error("Review Generated!")
        }
    }

    form_ele.submit((e)=>{
        e.preventDefault()
        $('textarea').val("");
        const form_data = new FormData(e.currentTarget)
        const data = Object.fromEntries(form_data)
        let copyReviewText = serverReq(url=location.pathname, method='POST', headers={"Content-Type":"application/json"}, body=JSON.stringify(data));
        
        copyReviewText.then((data)=>{
            $('textarea').val(data);
            let reviewCopyModal = new bootstrap.Modal(document.getElementById('reviewCopy'))
            reviewCopyModal.show()
        });
        
    })


    // Copy Review text using Library   ->  clipboard.min.js
    var clipboard = new ClipboardJS('#cc_review_text.cc_review_text');
    clipboard.on('success', function(e) {
        ReviewCopyAlert.classList.remove('d-none')
        setTimeout(() => {
            ReviewCopyAlert.classList.add('d-none')
        }, 3000);
        // e.clearSelection();
    });    
})