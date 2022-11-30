
function updateLang() {
    console.log("hello");
    let lang_val = $('#lang-more-options').val();
    if (lang_val != 'More options') {
        $('#lang-btns input[name=language]').val(lang_val);
        $('#lang-more-options').attr("style", "background-color:#ff9f46");

        lang_ids = ["btn-lang-English", "btn-lang-Spanish", "btn-lang-Unknown"];
        for (id of lang_ids) {
            let lang_btn = document.getElementById(id);
            console.log(lang_btn);
            if (lang_btn.hasAttribute("checked")) {
                lang_btn.removeAttribute("checked");
            }
        }

    }
}

function updateGender() {
    let gender_val = $('#gender-more-options').val();
    if (gender_val != 'More options') {
        $('#gender-btns input[name=gender]').val(gender_val);
        $('#gender-more-options').attr("style", "background-color:#ff9f46");

        gender_ids = ["btn-gender-Male", "btn-gender-Female", "btn-gender-Unknown"];
        for (id of gender_ids) {
            let gender_btn = document.getElementById(id);
            console.log(gender_btn);
            if (gender_btn.hasAttribute("checked")) {
                gender_btn.removeAttribute("checked");
            }
        }

    }
}

// function updateLang2() {
    
// }


function setup() {
    $('#lang-more-options').on('change', updateLang);
    $('#gender-more-options').on('change', updateGender);
}

$('document').ready(setup);