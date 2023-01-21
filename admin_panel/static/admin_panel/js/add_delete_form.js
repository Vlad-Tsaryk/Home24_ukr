    function add_form(form_name, copy_target_id,items_list_id, TotalForm ) {
        let currentFormCount = 0;
        let forms = $(`#${items_list_id} .form-${form_name}`)
        if (forms.length > 0) {
            currentFormCount = parseInt(forms.last().attr('id').split('-').pop()) + 1;
        }
        // console.log(currentFormCount)
        const copyEmptyFormEl = document.getElementById(copy_target_id).cloneNode(true)
        copyEmptyFormEl.setAttribute('id', `form-${form_name}-${currentFormCount}`)
        // console.log('#'+copyEmptyFormEl.id)
        const regex = new RegExp('__prefix__', 'g')
        copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
        TotalForm.attr('value', currentFormCount+1)
        $(copyEmptyFormEl).appendTo('#'+items_list_id).show()
        return copyEmptyFormEl
    }
    function delete_form(delete_id){
            $(`#id_${delete_id}-DELETE`).attr('checked','')
            $('#form-'+delete_id).hide()
    }