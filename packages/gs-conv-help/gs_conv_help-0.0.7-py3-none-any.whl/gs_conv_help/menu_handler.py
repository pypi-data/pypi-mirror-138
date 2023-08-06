#Handled by Alok
import warnings
from difflib import get_close_matches
from fuzzywuzzy import fuzz
from  . import gs_global
from .response_cards import show_response_card


warnings.filterwarnings('ignore')


def format_response_card_quick_reply(gs_context, current_context, response):
    response_json_quick = {}
    response_json_quick['content_type'] = 'image'
    response_json_quick["card_type"] = "quick_reply"
    response_json_quick["header"] = ""
    response_json_quick["body"] = response["title"]
    response_json_quick["caption"] = ""
    if response['url'] != 'None':
        response_json_quick['url'] = response["url"]
    else:
        response_json_quick['content_type'] = 'text'
        response_json_quick['url'] = ''
    filter_buttons = ['Invalid-choice-message', 'prompt',
                      'Card_Type', 'List_Header', 'List_Category', 'url']
    response["options"] = [
        x for x in response['options'] if x not in filter_buttons]
    response_json_quick["options"] = response["options"]
    show_response_card(gs_context, current_context, response_json_quick)


def format_response_card_list(gs_context, current_context, response, temp_menu):
    response_json_list = {}
    response_json_list['card_type'] = temp_menu['Card_Type']
    response_json_list['main_title'] = temp_menu['List_Header']
    response_json_list['main_body'] = response['title']
    response_json_list['button_text'] = "Show list"
    response_json_list["sections"] = []
    response_json_list_cat1 = {}
    response_json_list_cat1["title"] = temp_menu['List_Category']
    options = []
    filter_buttons = ['Invalid-choice-message', 'prompt', 'Card_Type',
                      'List_Header', 'Value_Description', 'List_Category']
    response["options"] = [
        x for x in response['options'] if x not in filter_buttons]
    if response['option_desc'] != 'None':
        lookup_desc_dict = response['option_desc']
    else:
        lookup_desc_dict = {}
    for button in response["options"]:
        each_option = {}
        each_option["title"] = button
        try:
            each_option['description'] = lookup_desc_dict[button]
        except:
            each_option['description'] = " "
        options.append(each_option)
    response_json_list_cat1["options"] = options

    response_json_list["sections"].append(response_json_list_cat1)
    show_response_card(gs_context, current_context, response_json_list)


def activate_menu(gs_context, current_context, selection):
    '''
        This function activates the handle active menu until
        the menu_handled is true.
    '''
    current_context['current_intent']['user_text'] = selection
    gs_context['active_menu'] = selection
    gs_context['menu_handled'] = True
    handle_active_menu(gs_context, current_context)
    return


def partial_match(x, y):
    return(fuzz.ratio(x, y))


def closest_matcher(word, options, gs_context, current_context):
    try:
        closest_match = (get_close_matches(word, options))[0]
    except:
        return word
    print("func closest_matcher ->>", closest_match, word)
    match_score = (fuzz.ratio(closest_match, word))
    print(match_score)
    if match_score > 80:
        return(closest_match)
    elif 40 < match_score < 80:
        response_json = {}
        response_json["card_type"] = "text"
        response_json["message"] = 'Did you mean this {}'.format(closest_match)
        show_response_card(gs_context, current_context, response_json)
        return(closest_match)
    else:
        return(word)


def handle_active_menu(gs_context, current_context):
    """
        This function will come handy when it is a live dictionary
    """

    if gs_context['menu_handled']:
        selection = current_context['current_intent']['user_text']
        db = gs_global.global_context['mongo_connection']
        temp_selection = selection.split(" ")
        if len(temp_selection) > 1 and temp_selection[-1].isdigit():
            selection = " ".join(temp_selection[:-1])
        if gs_context["slots"]['language']!='en':
            selection = db.reverse_translate(selection)
        response = {}
        if isinstance(gs_context['live_dict'], dict):
            available_key_live_dict = list(gs_context['live_dict'].keys())
        elif isinstance(gs_context['live_dict'], list):
            available_key_live_dict = gs_context['live_dict']
        selection = closest_matcher(
            selection, available_key_live_dict, gs_context, current_context)
        try:
            if selection in available_key_live_dict:
                temp_menu = gs_context['live_dict'][selection].copy()
                try:
                    # available dictionary
                    option_to_user = list(temp_menu.keys())
                    response['title'] = temp_menu['prompt']
                except:
                    option_to_user = temp_menu
                    response['title'] = 'Please select the options'
                gs_context['menu_handled'] = True
                option_to_user = [x for x in option_to_user if x not in [
                    'Invalid-choice-message', 'prompt']]

                if 'Category' not in option_to_user:
                    response['options'] = option_to_user
                    gs_context['live_dict'] = temp_menu
                    print('options without Category')
                    gs_context['active_menu'] = selection
                    gs_context['active_menu_state'].append(selection)
                else:
                    category_options = temp_menu['Category']
                    print('options with Category')
                    other_option = temp_menu.keys()
                    left_options = [
                        x for x in other_option if x not in ['Category']]
                    temp_temp_menu = {}
                    for key, value in temp_menu.items():
                        if key in left_options:
                            temp_temp_menu[key] = value
                    for keys in category_options:
                        temp_temp_menu[keys] = ''
                    gs_context['live_dict'] = temp_temp_menu
                    gs_context['active_menu'] = selection
                    gs_context['active_menu_state'].append(selection)
                    left_options.extend(category_options)
                    response['options'] = left_options
            else:
                temp_menu = gs_context['live_dict'].copy()
                response['title'] = gs_context['live_dict']['Invalid-choice-message']
                option_to_user = gs_context['live_dict'].keys()
                option_to_user = [x for x in option_to_user if x not in [
                    'Invalid-choice-message', 'prompt']]
                response['options'] = option_to_user
            if temp_menu['Card_Type'] == 'list':
                try:
                    response['option_desc'] = gs_context['live_dict']['Value_Description']
                except:
                    # Also handle this in the format_response_card_list
                    response['option_desc'] = 'None'
                format_response_card_list(
                    gs_context, current_context, response, temp_menu)
            else:
                try:
                    response['url'] = gs_context['live_dict']['url']
                except:
                    # Also change the card type to text
                    response['url'] = 'None'
                format_response_card_quick_reply(
                    gs_context, current_context, response)
        except Exception as e:
            if selection in gs_context['live_dict']:
                gs_context['active_menu_state'].append(selection)
                gs_context['menu_handled'] = False
                current_context["current_intent"] = {
                    'intent': 'Menu_Completed', 'entities': {}, 'user_text': ''}
            else:
                print('Thas is a wrong option please choose the one from the below')
                response['title'] = 'Thas is a wrong option please choose the one from the below'
                option_to_user = gs_context['live_dict']
                gs_context['menu_handled'] = True
                response['options'] = option_to_user
                temp_menu = option_to_user
                if temp_menu['Card_Type'] == 'list':
                    try:
                        response['option_desc'] = gs_context['live_dict']['Value_Description']
                    except:
                        # Also handle this in the format_response_card_list
                        response['option_desc'] = 'None'
                    format_response_card_list(
                        gs_context, current_context, response, temp_menu)
                else:
                    try:
                        response['url'] = gs_context['live_dict']['url']
                    except:
                        response['url'] = 'None'
                    format_response_card_quick_reply(
                        gs_context, current_context, response)
                return
        return
