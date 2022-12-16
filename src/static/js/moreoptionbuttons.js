
zips_data = $('#zipcodes_list').data("zipcodes");
zips_array = (((zips_data.slice(1, zips_data.length-1)).replace(/\s/g, '')).split(','));
zips_array.push(" Unknown ");

function updateLang() {
    console.log("hello");
    let more_ops_val = $('#lang-more-options').val();
    if (more_ops_val != 'More options') {
        $('#lang-btns input[name=language]').val(more_ops_val);
        $('#lang-more-options').attr("style", "background-color:#ff9f46");

        langs = ["lang-English", "lang-Spanish", "lang-Unknown"];
        // lang_labels = ["#toggle-lang-English", "#toggle-lang-Spanish", "#toggle-lang-Unknown"];
        for (lang of langs) {
            $("#btn-" + lang).prop("checked", false);
        }

    }
}

function updateGender() {
    let gender_val = $('#gender-more-options').val();
    if (gender_val != 'More options') {
        $('#gender-btns input[name=gender]').val(gender_val);
        $('#gender-more-options').attr("style", "background-color:#ff9f46");

        gender_ids = ["#btn-gender-Male", "#btn-gender-Female", "#btn-gender-Unknown"];
        for (id of gender_ids) {
            $(id).prop("checked", false);
        }

    }

}

function updateZip() {
    let zip_val = $('#text-zip-input').val();
    if (zip_val != '') {
        $('#zip-btns input[name=zip_codes]').val(zip_val);
        // $('#text-zip-input').attr("style", "background-color:#ff9f46");

        // zips_data = $('#zipcodes_list').data("zipcodes");
        // zips_array = ((zips_data.slice(1, zips_data.length-1)).replace(/\s/g, '')).split(',');
        // console.log(zips_array[zips_array.length-1].length);
        for (zip of zips_array) {
            $("#btn-zip-" + zip.slice(1, zip.length-1)).prop("checked", false);
        }

    }
}

function uncheckRaces() {
    console.log("unknown button is checked:" + $('#btn-race-Unknown').is(':checked'));
    if ($('#btn-race-Unknown').is(':checked')) {
        race_ids = ["#btn-race-White", "#btn-race-Black", "#btn-race-Hispanic"];
        for (id of race_ids) {
            $(id).prop("checked", false);
        }
        $('#race-multiselect').val(null).trigger('change');
    }
}

// function uncheckUnknown() {
//     if ($(e.target.id).is(':checked')) {
//         $('#btn-race-Unknown').prop("checked", false);
//     }
// }

function setup() {
    $('#lang-more-options').on('change', updateLang);
    $('#gender-more-options').on('change', updateGender);
    $('#text-zip-input').on('change', updateZip);
    
    $('#btn-race-Unknown').on('click', uncheckRaces);
    race_ids = ["#btn-race-White", "#btn-race-Black", "#btn-race-Hispanic"];
    for (id of race_ids) {
        $(id).on('click', function(e){
            console.log("in uncheck unknown");
            console.log($("#" + e.target.id).is(':checked'));
        
            if ($("#" + e.target.id).is(':checked')) {
                $('#btn-race-Unknown').prop("checked", false);
            }
        });
    }

    lang_ids = ["#btn-lang-English", "#btn-lang-Spanish", "#btn-lang-Unknown"];
    for (id of lang_ids) {
        $(id).on('click', function(e){
            let lang_val = $("#" + e.target.id).val();
            console.log(lang_val);
            // console.log("clicked on " + e.target.id);
            $('#lang-btns input[name=language]').val(lang_val);
            $('#lang-more-options').prop('style', 'background-color:white');
        });
    }

    gender_ids = ["#btn-gender-Male", "#btn-gender-Female", "#btn-gender-Unknown"];
    for (id of gender_ids) {
        $(id).on('click', function(e){
            let g_val = $("#" + e.target.id).val();
            console.log(g_val);
            $('#gender-btns input[name=gender]').val($("#" + e.target.id).val());
            $('#gender-more-options').prop('style', 'background-color:white');
        });
    }

    gender_ids = ["#btn-gender-Male", "#btn-gender-Female", "#btn-gender-Unknown"];
    for (id of gender_ids) {
        $(id).on('click', function(e){
            let g_val = $("#" + e.target.id).val();
            console.log(g_val);
            $('#gender-btns input[name=gender]').val($("#" + e.target.id).val());
            $('#gender-more-options').prop('style', 'background-color:white');
        });
    }

    for (zip of zips_array) {
        $("#btn-zip-" + zip.slice(1, zip.length-1)).on('click', function(e){
            let z_val = $("#" + e.target.id).val();
            console.log(z_val);
            $('#zip-btns input[name=zip_codes]').val($("#" + e.target.id).val());
            $('#text-zip-input').val('');
        });
    }

    $('#race-multiselect').select2({
        placeholder: "More options"
    }).on("select2:select", function(){$('#btn-race-Unknown').prop("checked", false);});
    
}

$('document').ready(setup);