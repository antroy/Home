var personal_count = 0;
var group_count = 0;

function reset(){
    personal_count = 0;
    group_count = 0;
    getElement("first_name").focus();
}

function findPos(obj) {
	var curleft = curtop = 0;
	if (obj.offsetParent) {
		curleft = obj.offsetLeft
		curtop = obj.offsetTop
		while (obj = obj.offsetParent) {
			curleft += obj.offsetLeft
			curtop += obj.offsetTop
		}
	}
	return [curleft,curtop];
}


function add_personal(){
    personal_count++;
    
    var type = 'p_' + personal_count + '_type';
    var value = 'p_' + personal_count + '_value';

    var edit_box = DIV({'class': 'contact_info'},
                        "Type: ",
                        INPUT({'type':'text', 'name': type, 'id': type, 
                               'class': 'combo',
                               'onclick': "toggle_type_dropdown('" + type + "', '" + value + "');",
                               'onfocus': "getElement('" + type + "').select();",
                               //'onblur': "hide_type_dropdown()",  
                               'onkeypress': "handle_keypress()"}),  
                        "    Details: ",
                        INPUT({'type':'text', 'class': 'details', 'id': value, 'name': value})   
               );
     
    appendChildNodes(getElement("personal_list"), edit_box);
    getElement(type).focus();
}

function add_group()
{
    group_count++;
    var prefix = 'a_' + group_count;
    var edit_box = DIV();

    appendChildNodes(getElement("group_list"), edit_box);
}


function handle_keypress(){
    
}

function fill_field(field, value){
    getElement(field).value = value;
    hide_type_dropdown();
}

function hide_type_dropdown(){
    dropdown = getElement("dropdown")
    dropdown.style.visibility = "hidden"
}

function toggle_type_dropdown(elmt, nextFocus){
    var element = getElement("dropdown");

    log("Vis: " + element.style.visibility)

    if (element.style.visibility == "visible"){
        hide_type_dropdown();
    }
    else {
        show_type_dropdown(elmt, nextFocus);
    }
}

function show_type_dropdown(elmt, nextFocus){
    var element = getElement(elmt);
    var pos = findPos(element);

    var make_link = function(value){
       return DIV({}, A({'href': "javascript:fill_field('" + elmt + "', '" + value + "');getElement('" + nextFocus + "').focus();"}, value)); 
    
    };

    var list = ["Phone", "Email", "Facebook", "LinkedIn", "Web", "Blog", "Fax"];
            
    dropdown = getElement("dropdown");
    
    var topval =  pos[1] + element.offsetHeight;
    var wid = element.offsetWidth - 5;

    dropdown.style.width = "" +  wid + "px";
    dropdown.style.left = "" + pos[0] + "px";
    dropdown.style.top = "" + topval + "px";

    dropdown.style.visibility = "visible";

    replaceChildNodes(dropdown, map(make_link, list));
}


/*
function show_edit_action(action_id){
    var edit = (action_id != null);

    if (edit)
    {
        var url = "./get_action_data?id=" + action_id;
        var d = loadJSONDoc( url );
        
        var callback = function (result) {
             text = result['text'];
             assigned_to = result['assigned_to'];
             display_dialog("edit_action", "action", action_id, text, assigned_to.id);
        }

        d.addCallback(callback);
    }
    else
    {
        display_dialog("add_action", "action", null, "", null);
    }
}

function get_options(assigned_to){
  var out = []
  #for $i, $user in enumerate($all_users)
     var d = {'value':'$user.id'};

     if ($user.id == assigned_to){
        d['selected'] = 'selected';
     }
     
     var opt = OPTION(d, '$user.display_name')
     
     out.push(opt);
  #end for

  return out;
}

function display_dialog(action, type, id, text, assigned_to){
    var type = type.toLowerCase();
    var edit_action = type == "action";
    var capit = type.substring(0,1).toUpperCase() + type.substring(1);
    var select = edit_action ? SELECT({'name': 'assign_to'}, get_options(assigned_to)) : null;
            
    var edit_box = DIV({'id': 'edit_box', 'class': "edit_dialog"},
                 FORM({'name': type + '_edit_form', 'action': action, 'method': 'POST'},
                   H2(null, "Edit " + capit),
                   INPUT({'type':'hidden', 'name': 'id', 'value': id}),
                   INPUT({'type':'hidden', 'name': 'item_id', 'value': $idea.id}),
                        select, 
                        TEXTAREA({'class':'small_edit_box', 'name': 'text'}, text),
                        INPUT({'type':'submit','value':'Update'}),  
                        INPUT({'type':'button','value':'Cancel', 
                                'onclick': 'javascript:removeElement("edit_box");'})   
                 )
               );
     
     appendChildNodes(currentDocument().body, edit_box);
}

function show_edit_note(id)
{
    var edit = (id != null);

    if (edit)
    {
        var url = "./get_note_data?id=" + id;
        var d = loadJSONDoc( url );
        
        var callback = function (result) {
             var text = result['text'];
             display_dialog("edit_note", "note", id, text, null);
        }

        d.addCallback(callback);
    }
    else
    {
        display_dialog("add_note", "note", null, "", null);
    }
}

function tab(hide_tab, show_tab, hide_id, show_id)
{
    swapElementClass(hide_tab, "tab_front", "tab_rear"); 
    swapElementClass(show_tab, "tab_rear", "tab_front"); 
    hideElement(hide_id);
    showElement(show_id);
    
}

function add_edit_update(action_id, update_id)
{
    var edit = (update_id != null); 
    var type = edit ? "Edit" : "Add";
    var button_text = edit ? "Update" : "Add New Update";
    var text = "";
    
    var display = function()
    {
        var edit_box = DIV({'id': 'add_edit_box', 'class': "edit_dialog"},
                     FORM({'name': 'add_edit_update_form', 'action': 'add_edit_update', 'method': 'POST'},
                       H2(null, type + " Action Update"),
                       INPUT({'type':'hidden', 'name': 'idea_id', 'value': $idea.id}),
                       INPUT({'type':'hidden', 'name': 'action_id', 'value': action_id}),
                       INPUT({'type':'hidden', 'name': 'update_id', 'value': update_id}),
                            TEXTAREA({'class':'small_edit_box', 'name': 'text'}, text),
                            INPUT({'type':'submit','value': button_text}),  
                            INPUT({'type':'button','value':'Cancel', 
                                    'onclick': 'javascript:removeElement("add_edit_box");'})   
                     )
                   );

         appendChildNodes(currentDocument().body, edit_box);
     }

    if (edit)
    {
        var url = "./get_action_update_data?id=" + update_id;
        var d = loadJSONDoc( url );
        
        var callback = function (result) {
             var text = result['text'];
             var assigned_to = result['assigned_to'];
             display();
        }

        d.addCallback(callback);
    }
    else
    {
        display();
    }
    
}
*/
