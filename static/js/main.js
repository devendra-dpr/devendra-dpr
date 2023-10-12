

$(document).ready(() => {
    // {% if questions %}
    // // Questions
    // {% for que in questions %}
    // {% if que[0] %}
    // var q{{ loop.index }}_ans_bad = {{ que[1]['bad'] | safe }}
    // var q{{ loop.index }}_ans_neutral = {{ que[1]['neutral'] | safe }}
    // var q{{ loop.index }}_ans_good = {{ que[1]['good'] | safe }}
    // {% endif %}
    // {% endfor %}
    let questions_list = []
    const star = "⚝"
    const star_fill = "⭐"
    const sm_star = "☆"
    const sm_star_fill = "★"

    const form_ele = $('form')
    const generate_review_text = $('form #generate_review_text')
    const question_form_error = document.querySelector('.question_form_error')
    
    
    async function serverReq(url, method = "GET", headers = {},) {
        const resp = await fetch(url, { method, headers })
        if (resp.ok){
            return await resp.json()
        }
        else{
            throw Error("No Questions Found!")
        }
    }


    let questionData =serverReq(location.pathname + "/question")
    questionData.then((data)=>{

        if (data.questions){
            console.log("data.questions : ", data.questions)
            questions_list = data.questions
            for (let i=0; i < data.questions.length; i++){
                if (data.questions[i].question_type === "simple_smile_rating"){
                    console.log("data.questions[q]question_type === simple_smile_rating", data.questions[i])
                    const q_ele = `
                    <div class="question">
                        <h6 class="question_text p-2 ">${data.questions[i].question}</h6>

                        <input type="radio" name="q${i}-simple_smile_rating" id="q${i}_bad" value="bad">
                        <label class="ans_bad" for="q${i}_bad"></label>

                        <input type="radio" name="q${i}-simple_smile_rating" id="q${i}_neutral" value="neutral">
                        <label class="ans_neutral" for="q${i}_neutral"></label>

                        <input type="radio" name="q${i}-simple_smile_rating" id="q${i}_good" value="good">
                        <label class="ans_good" for="q${i}_good"></label>
                    </div>`

                    // Appending Question in UI
                    form_ele.append(q_ele)
                }
                else if (data.questions[i].question_type === "simple_star_rating"){}
                else if (data.questions[i].question_type === "staff_smile_rating"){
                    console.log("data.questions[i].question_type === staff_smile_rating", data.questions[i])

                    let q_ele_staffs = ``
                    for (let j=0; j < data.questions[i]?.staffs.length; j++){
                        q_ele_staffs += `
                        <input type="radio" name="q${i}-staff_smile_rating-staff" id="q${i}_staff_${j}" value="${data.questions[i]?.staffs[j]}">
                        <label class="ans_staff" for="q${i}_staff_${j}">${data.questions[i]?.staffs[j]}</label>`
                    }
                    let q_ele = `
                        <div class="question col-12 mb-3">
                            <h6 class="question_text p-2 pb-0 ">which of our staff was good</h6>
                            <div class="row">
                                <div class="col-12 mb-3">
                                    ${q_ele_staffs}
                                </div>
                                <div class="col-12">
                                    <input type="radio" name="q${i}-staff_smile_rating" id="q${i}_bad" value="bad">
                                    <label class="ans_bad" for="q${i}_bad"></label>
            
                                    <input type="radio" name="q${i}-staff_smile_rating" id="q${i}_neutral" value="neutral">
                                    <label class="ans_neutral" for="q${i}_neutral"></label>
            
                                    <input type="radio" name="q${i}-staff_smile_rating" id="q${i}_good" value="good">
                                    <label class="ans_good" for="q${i}_good"></label>
                                </div>
                            </div>
                        </div>`
                    form_ele.append(q_ele)
                }
                else if (data.questions[i].question_type === "staff_star_rating"){}
            }
            form_ele.append(`<input type="submit" id="generate_review_text" class="btn btn-primary mb-2" value="Generate Review" />`)
            // Hide the TEXT `No Questions Found!`
            question_form_error.classList.add('d-none')
        }
    }).catch((e)=>{
        // console.log(e.message, e)
        question_form_error.classList.remove('d-none')
        question_form_error.textContent = e.message
    })

    form_ele.submit((e)=>{
        e.preventDefault()
        console.log(e)
        let copyReviewText = ``
        const submitter = document.querySelector("#generate_review_text")
        const form_data = new FormData(e.currentTarget, submitter)
        console.log(form_data, typeof form_data, form_data.get("q2-staff_smile_rating-staff"))
        console.log(submitter)

        for (const [key, value] of form_data) {
            // console.log(`${key}: ${value}\n`);
            const q_slit = key.split("-")
            if (q_slit[2] === "staff"){
                continue
            }
            else{
                const review = getReview(q_index=q_slit[0].slice(1), q_value=value, q_type=q_slit[1], form_data)
                copyReviewText += review
            }
        }
        $('textarea').val(copyReviewText)
        let reviewCopyModal = new bootstrap.Modal(document.getElementById('reviewCopy'))
        reviewCopyModal.show()
    })

    // get random review value of question
    function getReview(q_index, q_value, q_type, form){
        const is_staff_q = ['staff_smile_rating', "staff_star_rating"].find((q_typ)=>q_typ === q_type)
        
        let staff = ''
        if (is_staff_q){        // Getting Staff Name
            staff = form.get(`q${q_index}-${q_type}-staff`)
        }


        if (q_type == "simple_star_rating"){       // simple_star_rating
            console.log("question is -> simple_star_rating", q_value);
        }
        else if (q_type == "staff_smile_rating"){       // staff_smile_rating
            // console.log("question is -> staff_smile_rating", q_value, staff);
            let review = get_sugg_review(questions_list[q_index].sugg[q_value])
            review = review.replaceAll("STAFF_NAME", staff);
            return review.trim()
        }
        else if (q_type == "staff_star_rating"){       // staff_star_rating
            console.log("question is -> staff_star_rating", q_value, staff);
        }
        else{       // simple_smile_rating
            // console.log("question is -> simple_smile_rating", q_value);
            const review = get_sugg_review(questions_list[q_index].sugg[q_value])
            return review.trim()

        }
    }

    function get_sugg_review(suggs) {
        const ans_index = Math.floor(Math.random() * suggs.length);
        return suggs[ans_index]
    }

    // Copy Review text using Library   ->  clipboard.min.js
    var clipboard = new ClipboardJS('#cc_review_text.cc_review_text');













    // form_ele.on('click', '#generate_review_text', (e)=>{
    //     e.preventDefault
    //     console.log("generate_review_text : ")
    // })

    // $.ajax({
    //     url: location.pathname + "/question",
    //     method: "GET",
    //     success: (data, status, xhr) => {
    //         console.log("question : ", data)
    //     },
    //     error: (xhr, status, error) => {
    //         console.log(xhr, status, error)
    //     }
    // })


    // //  Generating a random review from given above list based on action of the user
    // $('#generate_review_text').click((event) => {
    //     let copyReviewText = ``
    //     {% for que in questions %}
    //     {% if que[0] %}
    //     const q{{ loop.index }}_customer_ans = $("input[type='radio'][name='q{{ loop.index }}']:checked").val();
    //     {% endif %}
    //     {% endfor %}

    //     {% for que in questions %}
    //     {% if que[0] %}
    //     if (q{{ loop.index }}_customer_ans != undefined) {
    //         if (q{{ loop.index }}_customer_ans == "good") {     // Review is Good
    //             const ans_index = Math.floor(Math.random() * q{{ loop.index }}_ans_good.length);
    //             copyReviewText = copyReviewText.trim() + " " + q{{ loop.index }}_ans_good[ans_index]

    //             console.log("q{{ loop.index }} Good: ", q{{ loop.index }}_ans_good[ans_index])
    //         }
    //         else if (q{{ loop.index }}_customer_ans == "neutral") {     // Review is Neutral
    //             const ans_index = Math.floor(Math.random() * q{{ loop.index }}_ans_neutral.length);
    //             copyReviewText = copyReviewText.trim() + " " + q{{ loop.index }}_ans_neutral[ans_index]

    //             console.log("q{{ loop.index }} Neutral: ", q{{ loop.index }}_ans_neutral[ans_index])
    //         }
    //         else if (q{{ loop.index }}_customer_ans == "bad") {     // Review is Bad
    //             const ans_index = Math.floor(Math.random() * q{{ loop.index }}_ans_bad.length);
    //             copyReviewText = copyReviewText.trim() + " " + q{{ loop.index }}_ans_bad[ans_index]
    //             console.log("q{{ loop.index }} Bad: ", q{{ loop.index }}_ans_bad[ans_index])
    //         }
    //     }
    //     {% endif %}
    //     {% endfor %}

    //     $('textarea').val(copyReviewText)
    //         // Copy the text inside the text field
    //         // navigator.clipboard.writeText(data);

    //         // Alert the copied text
    //         // alert("Copied the text: " + data);
    //     let reviewCopyModal = new bootstrap.Modal(document.getElementById('reviewCopy'))
    //     reviewCopyModal.show()
    // })

    // // Copy Review text using Library   ->  clipboard.min.js
    // var clipboard = new ClipboardJS('#cc_review_text.cc_review_text');
    // {% endif %}
})