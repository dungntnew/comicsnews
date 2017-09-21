'use strict';

function setupJsonEditor(selector) {
    var json_textarea = $(selector);
    var json_editor = $(json_textarea).parent()[0];
    var init_json_text = $(json_textarea).text();

    // Set the default CSS theme and icon library globally
    JSONEditor.defaults.theme = 'bootstrap3';
    JSONEditor.defaults.iconlib = 'fontawesome4';

     // This is the starting value for the editor
     // We will use this to seed the initial editor
     // and to provide a "Restore to Default" button.
    var starting_value = JSON.parse(init_json_text) || {}

       // Initialize the editor
      var editor = new JSONEditor(json_editor,{
        // Enable fetching schemas via ajax
        ajax: false,
        refs: {},
        schema: {
           format: "grid"
        },
        startval: starting_value,
        collapsed: true,
        expand_height: true,
      });


    // Hook up the validation indicator to update its
    // status whenever the editor changes
    editor.on('change',function() {
        // Get an array of errors from the validator
        var errors = editor.validate();


        // Not valid
        if(errors.length) {
        }
        // Valid
        else {
           $(json_textarea).text(JSON.stringify(editor.getValue()));
        }
    });
}

jQuery(document).ready(function(){
    if ($('.json-raw-text').length !== 0) {
        setupJsonEditor('.json-raw-text');
    }
});