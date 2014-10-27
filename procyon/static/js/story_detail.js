var story_details = {};
story_details.MEDIA_PREFIX = "/site_media/media/";
story_details.default_story = {variables: [], story: [], choices: [], requirements: []};
story_details.all_images = {};
story_details.show_parsed_variables = true;
story_details.show_choices_as_tree = true;
story_details.choice_tree_shrink = false;
story_details.new_tree_node_text = "-New Node-";
story_details.$tree_node_holder = null;
story_details.$tree = null;

//TODO: Pick variables in event variables list
//TODO: Generate random variables from generators
//TODO: View Grpahically with map background
//TODO: Textboxes, WYSIWYG viewers for story text
//TODO: Create new story

//-------------------------------------
story_details.suggested = {};

story_details.suggested.values = "epic fantastic superb great good fair average mediocre poor terrible none".split(" ");
story_details.suggested.requirement_concept = "world city character".split(" ");
story_details.suggested.requirement_name = {
    world: "magic technology war culture".split(" "),
    city: "near defense offense culture religion ocean wealth science industry".split(" "),
    character: "strength constitution dexterity intelligence wisdom charisma luck health wealth".split(" ")  //TODO: Use Fate?
};
story_details.suggested.effect_function = "characterGainsMoney characterGainsServant characterGainsTreasure characterWounded battle familyCursed familyBlessed".split(" "); //TODO: Auto add:  worldDecreaseMagic worldIncreaseMagic worldIncreaseTechnology worldDecreaseTechnology worldIncrease
story_details.suggested.variable_kind = "item character location animal pet friend spell skill knowledge business child".split(" ");
//-------------------------------------

story_details.schema = {
    requirements: [
        {field: "concept", options: story_details.suggested.requirement_concept, required: true, type: "options", default: "world"},
        {field: "name", required: true, type: "options-suggested", options_relate_to: "concept", heading: true, default: "magic", options: story_details.suggested.requirement_name},
        {field: "has", type: "string"},
        {field: "exceeds", default: "mediocre", type: "options-suggested", options: story_details.suggested.values},
        {field: "below", type: "options-suggested", options: story_details.suggested.values},
        {field: "is", type: "string"}
    ],
    effects: [
        {field: "function", required: true, type: "options-suggested", heading: true, default: "characterGainsMoney", options: story_details.suggested.effect_function},
        {field: "variable", type: "string"},
        {field: "value", type: "options-suggested", options: story_details.suggested.values}
    ],
    variables: [
        {field: "name", required: true, type: "string", default: "gem"},
        {field: "nickname", required: true, heading: true, type: "string", default: "Azure sparkling Gemstone"},
        {field: "tags", type: "string"},
        {field: "title", type: "string"},
        {field: "value", type: "options-suggested", options: story_details.suggested.values},
        {field: "kind", type: "options", required: true, options: story_details.suggested.variable_kind, default: "item"},
        {field: "subkind", type: "string"},
        {field: "strength", type: "options-suggested", options: story_details.suggested.values}, //TODO: Rethink this for use in fighting games...
        {field: "defense", type: "options-suggested", options: story_details.suggested.values},
        {field: "armor", type: "string"},
        {field: "weapons", type: "string"}
    ],
    story: [
        {field: "text", heading: true, required: true, type: "textblock", default: "'Twas a dark and story night..."}
    ],
    stories: [
        {field: "name", required: true, type: "string", default: "Something important happened...", heading: true},
        {field: "anthology", required: true, type: "string", default: "Everywhere"},
        {field: "tags", type: "string"},
        {field: "active", type: "boolean"},
        {field: "max_times_usable", type: "integer"},
        {field: "year_max", type: "integer"},
        {field: "year_min", type: "integer"},
        {field: "force_usage", type: "integer"},
        {field: "description", type: "textblock", default: "Summary of story"}
    ],
    chances: [
        {field: "title", heading: true, required: true, type: "textblock", default: "This is what happens..."}
    ],
    choices: [
        {field: "title", heading: true, required: true, type: "textblock", default: "You can choose to..."}
    ],
    images: [
        {field: "url", heading: true, required: true, type: "string", default: "image_name"}
    ]
};
story_details.defaultObjectOfType = function (type) {
    var data = {};
    var schema = story_details.schema[type] || story_details.schema[type+"s"] || {};
    _.each(schema, function (schemata) {
        if (schemata.required) {
            data[schemata.field] = schemata.default;
        }
    });
    return data;
};

//=======================================
story_details.init = function (story) {
//    story_details.schema.requirements[1].options = _.flatten(_.toArray(story_details.suggested.requirement_name));

    story = story || story_details.default_story;

    //Link all images into the class object
    story_details.all_images = story.images;

    story_details.drawStory(story);

    $(document).on('showalert', '.alert', function(){
        window.setTimeout($.proxy(function() {
            $(this).fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
            });
        }, this), 5000);
})

};
story_details.drawStory = function (story) {
    story = story || story_details.default_story;

    //Draw story complex details
    $("#story, #choices, #variables, #downloads").empty();

//    $("#requirements").append(story_details.buildRequirementsHolder(story.requirements));

    story_details.showVariables(story.variables);
    story_details.showStory(story.story);
    story_details.buildDownloadButtons();

    var $choices = $("#choices");
    if (story_details.show_choices_as_tree) {
        var $tree = $("<div>").attr('id', 'story_tree').appendTo($choices);
        var $tree_node_holder = story_details.$tree_node_holder = $("<div>").appendTo($choices);
        story_details.treeFromData(story, $tree, $tree_node_holder);
        $('#variables').hide();
    } else {
        $choices.append(story_details.buildChoices(story.choices));
        $('#variables').show();
    }

};
story_details.showStory = function (data) {
    var $story = $("#story");
    data = data || [];
    _.each(data, function (story) {
        var text = story_details.nodeTexts.story(story);
        if (text) {
            $("<div>")
                .addClass("story_text")
                .html(text)
                .appendTo($story);
        }
        $story.append(story_details.buildImagesHolder(story.images));
    });
};

//Tis is the older div-based layout. Possibly delete if tree works well
story_details.buildChoices = function (choices) {
    var $holder = $("<div>");

    _.each(choices || [], function (choice) {
        var $opt = $("<div>")
            .addClass('choice_holder')
            .appendTo($holder);

        var title = "Player choice: <b>" + story_details.nodeTexts.choice(choice) + "</b>";
        $("<span>")
            .addClass('choice_title')
            .html(title)
            .appendTo($opt);

        $opt.append(story_details.buildRequirementsHolder(choice.requirements));
        $opt.append(story_details.buildEffectsHolder(choice.effects));

        var chances = choice.chances || [];
        var num_chances = chances.length;
        //TODO: Loop through each and find total probability

        _.each(chances, function (chance) {
            var percent = parseInt(100 / num_chances);
            var $sub_opt = $("<div>")
                .html(percent + "% : " + story_details.text(chance.title))
                .addClass("chance spacer")
                .appendTo($opt);

            $sub_opt.append(story_details.buildRequirementsHolder(chance.requirements));
            $sub_opt.append(story_details.buildEffectsHolder(chance.effects));

            if (chance.choices) {
                $sub_opt.append(story_details.buildChoices(chance.choices));
            }
        });

    });
    return $holder;
};
story_details.showVariables = function (data) {
    var $vars = $("#variables");
    data = data || [];
    _.each(data, function (variable) {
        var header = story_details.nodeTexts.variable(variable);
        var $var = $("<div>")
            .html(header)
            .appendTo($vars);

        if (variable.details) {
            $var
                .css("cursor", "hand")
                .attr("title", variable.details);
        }

    });
};

// --- HTML Holder Builders
story_details.buildEffectsHolder = function (effects) {
    var $effects_holder = $("<span>");
    _.each(effects, function (effect) {
        var text = "<b>" + story_details.nodeTexts.effect(effect) + "</b> ";
        $("<span>")//TODO: Pass it text and not have nested spans
            .html(text)
            .addClass('effect')
            .appendTo($effects_holder);
    });
    return $effects_holder;
};

story_details.nodeTexts = {};
story_details.nodeTexts.requirement = function (node) {
    var text = (node.concept || "default") + "." + node.name;
    if (node.has) {
        text += " has a value in it of " + node.has;
    } else if (node.exceeds) {
        text += " >= " + node.exceeds;
    } else if (node.below) {
        text += " <= " + node.below;
    } else if (node.is) {
        text += " = " + node.is;
    } else if (node.isnt) {
        text += " is not = " + node.isnt;
    } else {
        text += " is set and isn't 0";
    }
    return text;
};
story_details.nodeTexts.image = function (image) {
    var allImages = story_details.all_images;
    var url = null;

    if (_.isString(image) && _.str.startsWith(image, "http")) {
        url = image;
    } else if (image && image.url && _.str.startsWith(image.url, "http")) {
        url = image.url;
    } else if (image && image.url) {
        _.each(allImages, function (imageLookup) {
            if (imageLookup.url.indexOf(image.url) > 0) {
                url = story_details.MEDIA_PREFIX + imageLookup.url;
            }
        });
        if (!url) url = image.url;
    }
    return url;
};
story_details.nodeTexts.story = function (stories) {
    var text = "";
    if (!_.isArray(stories)) stories = [stories];

    _.each(stories, function (story) {
        if (story && story.text) {
            text += story.text;
        }
    });
    return story_details.text(text);
};
story_details.nodeTexts.chance = function (node, percent) {
    var text = "";
    if (percent) {
        text = percent + "%: ";
    }
    text += (node.title || "Default");
    return text;
};
story_details.nodeTexts.effect = function (effect) {
    var text = effect.function || "effect";
    if (effect.value) {
        text += "(" + effect.value + ")";
    }
    if (effect.variable) {
        text += "(" + story_details.text(effect.variable) + ")";
    }
    return text;
};
story_details.nodeTexts.variable = function (variable) {
    var text = "[" + variable.nickname + "]: " + variable.name + ", Type: " + variable.type;
    if (variable.subtype) {
        text += " (" + variable.subtype + ")";
    }
    if (variable.tags) {
        text += " (" + variable.tags + ")"; //TODO: Click on each to filter
    }
    return text;
};
story_details.nodeTexts.choice = function (choice) {
    return story_details.text(choice.title);
};

//---------------------

story_details.buildRequirementsHolder = function (data) {
    var $holder = $("<span>");
    data = data || [];
    _.each(data, function (requirement) {
        var text = "<b>" + story_details.nodeTexts.requirement(requirement) + "</b> ";
        $("<span>")
            .addClass('requirement')
            .attr('title', "Requires")
            .html(text)
            .appendTo($holder);
    });
    return $holder;
};
story_details.buildImagesHolder = function (data) {
    var $holder = $("<span>");
    _.each(data, function (image) {
        var url = story_details.nodeTexts.image(image);
        if (url) {
            $("<img>")
                .attr('src', url)
                .appendTo($holder);
        }
    });
    return $holder;
};


story_details.buildDownloadButtons = function () {
    var $downloads = $('#downloads');
    $("<a>")
        .addClass('btn download')
        .text("Download Story as JSON")
        .on('click', function () {
            var obj = story_details.default_story;
            var data = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));
            window.open(data, 'story_' + obj.id);
        })
        .appendTo($downloads);

    $("<a>")
        .addClass('btn')
        .text("Toggle Parsed Variables")
        .on('click', function () {
            story_details.show_parsed_variables = !story_details.show_parsed_variables;
            story_details.drawStory();
        })
        .appendTo($downloads);

    $("<a>")
        .addClass('btn')
        .text("Show choices Differently")
        .on('click', function () {
            story_details.show_choices_as_tree = !story_details.show_choices_as_tree;
            story_details.drawStory();
        })
        .appendTo($downloads);

    $("<a>")
        .addClass('btn btn-warning')
        .text("Toggle Tree Editability")
        .on('click', function () {
            story_details.choice_tree_shrink = !story_details.choice_tree_shrink;
            story_details.drawStory();
        })
        .appendTo($downloads);

    $("<a>")
        .addClass('btn btn-success')
        .attr('id','btn_submit')
        .text("Submit Changes")
        .on('click', function () {

            $.ajax({
                url: '',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(story_details.default_story),
                dataType: 'text',
                success: function (result) {
                    result = JSON.parse(result);
                    if (result && result.status=="OK") {
                        $('<div class="alert alert-success">Update Saved</div>').appendTo('#downloads').trigger('showalert');
                    } else {
                        $('<div class="alert alert-error">Error - Update Not Saved</div>').appendTo('#downloads').trigger('showalert');
                    }
                    console.log(result);
                }
            });
        })
        .appendTo($downloads);

};

story_details.text = function (text) {
    return (story_details.show_parsed_variables ? story_details.replaceParsedVariables(text) : text);
};
story_details.replaceParsedVariables = function (text, variables) {
    variables = variables || story_details.default_story.variables;

    //Look for variables in text. If found, loop through each and replace them in text
    var var_finder = new RegExp("\[[\\w:]+\]", "ig");
    var matches = var_finder.exec(text);
    if (matches && matches.length) {
        _.each(matches, function (match) {
            _.each(variables, function (v) {
                if (v.nickname && match.indexOf(v.nickname) > 0 && text.indexOf("[" + v.nickname) > -1) {
                    //This is the variable described

                    var var_finder = new RegExp("\\[" + v.nickname + "\\]", "ig");
                    text = text.replace(var_finder, "<b>" + v.nickname + "</b>");

                    _.each('name tags value subtype type details'.split(" "), function (field) {
                        if (v[field]) {
                            var var_finder = new RegExp("\\[" + v.nickname + ":" + field + "\\]", "ig");
                            text = text.replace(var_finder, "<b>" + v[field] + "</b>");
                        }

                    });
                }
            });
        })
    }

    return text;
};

//------------------------------------

story_details.treeFromData = function (story, $treeHolder, $tree_node_holder) {

    var nodeIsNotFolder = function (node) {
        return !(node.text && !node.data);
    };
    var buildANode = function (parent, text, type, tree, data) {
        var new_node = tree.create_node(parent,{text: text},"first");

        var outputNode = story_details.titleNodeFromType(data,type);

        if (outputNode.icon) {
            tree.set_icon(new_node, outputNode.icon);
        }

        var new_node_pointer = tree.get_node(new_node);
        if (outputNode.a_attr && outputNode.a_attr.class) {
            new_node_pointer.a_attr = new_node_pointer.a_attr || {};
            new_node_pointer.a_attr.class = new_node_pointer.a_attr.class || "";
            new_node_pointer.a_attr.class += " " + outputNode.a_attr.class;
            new_node_pointer.a_attr.class = _.str.trim(new_node_pointer.a_attr.class);
        }

        if (data) {
            new_node_pointer.data = data;
            tree.edit(new_node, text);
        }
        story_details.showNodeDetail(new_node_pointer, $tree_node_holder);

        tree.deselect_all();
        tree.select_node(new_node);
    };
    var preventSubFolders = function (node, parent_type) {
        var type = treeNodeStoryType(node);
        //Only allow choices aad chances to be added below the root level
        return !nodeIsNotFolder(node)
            || (node.parent == "#")
            || (type == "requirement")
            || (type == "variable");
//            || (type == "effect")
//            || (node.text == story_details.new_tree_node_text)
//            || (type == parent_type);
    };
    var treeNodeStoryType = function (node) {
        var type = (node.data) ? node.data.type : node.text || null;

        type = type ? type.toLowerCase() : null;

        if (type == "requirements") {
            type = "requirement"
        } else if (type == "choices") {
            type = "choice";
        } else if (type == "chances") {
            type = "chance";
        } else if (type == "effects") {
            type = "effect";
        } else if (type == "variables") {
            type = "variable";
        }
        return type;
    };
    var baseDataFromType = function (type) {
        var data = story_details.defaultObjectOfType(type);
        if (data && !_.isEmpty(data)) {
            data.type = type;
        } else {
            data = null;
        }
        return data;
    };

    var customMenu = {
        "items": function (node) {
            var tree = $treeHolder.jstree(true);
            return {
                "AddRequirements": {
                    "separator_before": false,
                    "separator_after": false,
                    "label": "Add Requirements",
                    "_disabled": function () {
                        return preventSubFolders(node, 'requirement');
                    },
                    "action": function () {
                        buildANode(node, 'Requirements', 'tree_header', tree)
                    }
                },
                "AddChoices": {
                    "separator_before": false,
                    "separator_after": false,
                    "label": "Add Choices",
                    "_disabled": function () {
                        return preventSubFolders(node, 'choice');
                    },
                    "action": function () {
                        buildANode(node, 'Choices', 'tree_header', tree)
                    }
                },
                "AddChances": {
                    "separator_before": false,
                    "separator_after": false,
                    "label": "Add Chances",
                    "_disabled": function () {
                        return preventSubFolders(node, 'chance');
                    },
                    "action": function () {
                        buildANode(node, 'Chances', 'tree_header', tree)
                    }
                },
                "AddEffects": {
                    "separator_before": false,
                    "separator_after": false,
                    "label": "Add Effects",
                    "_disabled": function () {
                        return preventSubFolders(node, 'effect');
                    },
                    "action": function () {
                        buildANode(node, 'Effects', 'tree_header', tree)
                    }
                },
                "AddVariables": {
                    "separator_before": false,
                    "separator_after": false,
                    "label": "Add Variables",
                    "_disabled": function () {
                        return node.id != "j1_2";
                    },
                    "action": function () {
                        buildANode(node, 'Variables', 'tree_header', tree)
                    }
                },
                "AddItem": {
                    "separator_before": false,
                    "separator_after": false,
                    "label": "Add Item",
                    "_disabled": function () {
                        return nodeIsNotFolder(node) || (node.text == story_details.new_tree_node_text);
                    },
                    "action": function () {
                        var type = treeNodeStoryType(node);
                        buildANode(node, story_details.new_tree_node_text, type, tree, baseDataFromType(type))
                    }
                },
                "Rename": {
                    "separator_before": true,
                    "separator_after": false,
                    "label": "Rename",
                    "_disabled": function () {
                        return !nodeIsNotFolder(node);
                    },
                    "action": function () {
                        tree.edit(node);
                    }
                },
                "Remove": {
                    "separator_before": true,
                    "separator_after": false,
                    "label": "Delete",
                    "action": function () {
                        tree.delete_node(node);
                    }
                }
            };
        }
    };

    var pluginsToUse = ["wholerow", "dnd"];
    if (!story_details.choice_tree_shrink) {
        pluginsToUse.push("contextmenu");
    }

    var data = story_details.convertStoryToTree(story, "stories");
    story_details.$tree = $treeHolder.jstree({
        plugins: pluginsToUse,
        ui: {
            select_limit: 1
        },
        contextmenu: customMenu,
        core: {
            data: data,
            check_callback: true
        }
    });
    $tree_node_holder
        .addClass("tree_detail");

    $treeHolder.on("select_node.jstree",
        function (evt, holder) {
            var node = holder.node || {};
            story_details.showNodeDetail(node, $tree_node_holder);
        }
    );
    $treeHolder.on("rename_node.jstree",
        function (evt, holder) {
            var node = holder.node || {};
            var data = node.data || {};
            var newText = node.text || "unknown";
            var type = data.type || "unknown";
            var field = "";

            if (type == "requirement") {
                field = "name"
            } else if (type == "choice") {
                field = "title";
            } else if (type == "chance") {
                field = "title";
            } else if (type == "effect") {
                field = "function";
            } else if (type == "variable") {
                field = "nickname";
            }

            node.data[field] = newText;
            story_details.showNodeDetail(node, $tree_node_holder);
            story_details.transformTreeToStory();
//            story_details.$tree.jstree('refresh');
        }
    );

};
story_details.showNodeDetail = function (node, $tree_node_holder) {
    $tree_node_holder = $tree_node_holder || story_details.$tree_node_holder;
    var data = node.data || {};
    var variables_already_set = [];

    $tree_node_holder.empty();
    if (data && !_.isEmpty(data)) {
        for (key in data) {
            var val = data[key];
            if (!_.isArray(val) && !_.isObject(val)) {
                if (key != "type") variables_already_set.push(key);
            }
        }
        //TODO: Set if options are linked and one is set to change other options

        var schema = story_details.schema[data.type] || story_details.schema[data.type+"s"] || [];
        _.each(schema,function(schema_item){
            story_details.buildEditControl(schema_item,node).appendTo($tree_node_holder);
        });

    } else {
        //It's an array holder
        var text = node.text;
        if (text) {
            $("<span>")
                .html("<b>Folder of " + text + "</b>")
                .appendTo($tree_node_holder);
        }
    }
};

story_details.titleNodeFromType = function(storyItem, type) {
    type = type || storyItem.type || "unknown";
    storyItem = storyItem || {};

//    var output = {state: {}, text:""};
    var output = {state: {opened: true}, text:""};
    if (type == "stories") {
        output.text = storyItem.name || storyItem.description || "Story";
    } else if (type == "story") {
        output.text = story_details.nodeTexts.story(storyItem.story);
        output.icon = "/static/icons/story.png";
    } else if (type == "images" || type == "image") {
        output.text = story_details.nodeTexts.image(storyItem);
        output.icon = "/static/icons/image.png";
    } else if (type == "chances" || type == "chance") {
        //TODO: Incorporate parseInt(100 / num_chances);
        output.text = story_details.nodeTexts.chance(storyItem);
        output.state = {opened: false};
        output.a_attr = {class: 'chance bold'};
        output.icon = "/static/icons/chance.png";
    } else if (type == "effects" || type == "effect") {
        output.text = story_details.nodeTexts.effect(storyItem);
        output.a_attr = {class: 'effect'};
        output.icon = "/static/icons/star_empty.png";
    } else if (type == "requirements" || type == "requirement") {
        output.text = story_details.nodeTexts.requirement(storyItem);
        output.a_attr = {class: 'requirement'};
        output.icon = "/static/icons/question.png";
    } else if (type == "variables" || type == "variable") {
        output.text = story_details.nodeTexts.variable(storyItem);
        output.icon = "/static/icons/gem.png";
    } else if (type == "choices" || type == "choice") {
        output.text = story_details.nodeTexts.choice(storyItem);
        output.a_attr = {class: 'choice bold'};
        output.icon = "/static/icons/choice.png";
    }
    if (!output.text && storyItem.text) {
        output.text = story_details.text(storyItem.text);
    }
    if (story_details.choice_tree_shrink) {
        output.text = "<b>" + _.str.titleize(type) + "</b>: " + output.text;
    }
    return output;
};

story_details.convertStoryToTree = function (stories, type) {
    if (_.isObject(stories) && !_.isArray(stories)) {
        stories = [stories]; //Make sure it's an array
    }

    var nodeList = [];
    _.each(stories, function (storyItem) {
        nodeList.push(story_details.convertNodeToStoryNode(storyItem, type));
    });

    var result;
    if (story_details.choice_tree_shrink) {
        result = nodeList;
    } else {
        result = {text: _.str.titleize(type), children: nodeList, state: {opened: true}, a_attr: {class: 'tree_header'}}
    }

    return result;
};
story_details.convertNodeToStoryNode = function (storyItem, type) {
    if (_.isArray(storyItem)) {
        console.error("convertNodeToStoryNode - An Array was passed in through an array in a story item");
        console.error(storyItem);
        return storyItem;
    }
    var output = story_details.titleNodeFromType(storyItem,type);
    var children = [];

    //For each item, add children if there is a sub-tree
    _.each("story,images,requirements,chances,choices,effects,variables".split(","), function (key) {
        var val = storyItem[key];
        if (val) {
            var node = story_details.convertStoryToTree(val, key);
            if (node) children.push(node);
        }
    });

    output.text = _.str.truncate(output.text || "Unrecognized item", 80);

    if (story_details.choice_tree_shrink) {
        children = _.flatten(children);
    }
    output.children = (children && children.length) ? children : null;
    storyItem.type = type;
    output.data = storyItem;

    return output;
};
story_details.transformTreeToStory = function ($tree) {
    $tree = $tree || story_details.$tree;
    var data = $tree.jstree().get_json();

    var json = story_details.exportTreeNode(data);
    var story = json[0].stories[0];

    story_details.default_story = story;
};
story_details.exportTreeNode = function (data) {
    var output = [];
    _.each(data, function (item) {
        var obj = item.data;
        var output_obj = {};
        if (_.isObject(obj) && _.isEmpty(obj) && item.children) {
            var title = item.text.toLowerCase();
            output_obj[title] = story_details.exportTreeNode(item.children);
        } else if (_.isObject(obj) && item.children) {
            for (key in obj) {
                var val = obj[key];
                if (val && !_.isArray(val) && !_.isObject(val)) {
                    output_obj[key] = obj[key];
                }
            }
        }
        _.each(item.children, function (nodeGroup) {
            var title = nodeGroup.text.toLowerCase();
            output_obj[title] = story_details.exportTreeNode(nodeGroup.children);
        });

        if (output_obj) {
            output.push(output_obj);
        }
    });
    return output;
};
story_details.buildEditControl = function(schema_item, node) {
    var $div = $("<div>");
    var $control, $control2;
    var field = schema_item.field || "Field";
    var $label = $("<label>")
        .text(_.str.titleize(field) + ": ")
        .appendTo($div);
    if (schema_item.required) $label.css({textWeight:"bold"});

    var name = "edit_control_"+field;
    if (schema_item.type == "options-suggested" || schema_item.type == "options") {
        $control = $("<select>")
            .attr({
                id:name,
                name:name
            })
            .addClass("edit_input")
            .appendTo($div);
        var opts = schema_item.options || [];
        if (schema_item.options_relate_to) {
            //Use the options depending on what another var is set to
            var related = $("#edit_control_" + schema_item.options_relate_to).val();
            var new_opts = [];
            if (related) {
                for (key in opts) {
                    if (key.toLowerCase() == related.toLowerCase()) {
                        new_opts = opts[key];
                    }
                }
                opts = new_opts;
            }
        }

        if (!schema_item.required) {
            opts = [" "].concat(opts);
        }
        var existing = node.data[field];
        var foundExisting = false;
        _.each(opts,function(option){
            var $opt = $("<option>")
                .val(option)
                .text(option)
                .appendTo($control);
            if (existing && option == existing) {
                $opt.attr('selected',true);
                foundExisting = true;
            }
        });
        if (!foundExisting && existing && _.isString(existing) && existing.trim()) {
            $("<option>")
                .val(existing)
                .text(existing)
                .attr('selected',true)
                .appendTo($control);
        }
        if (schema_item.type == "options-suggested") {
            $("<span>or</span>")
                .appendTo($div);
            $control2 = $("<input>")
                .attr({
                    type:"text",
                    id:name+"_text",
                    name:name+"_text"
                })
                .addClass("edit_input")
                .appendTo($div);
            if (node.data[field]) {
                $control2.val(node.data[field]);
            }

        }
    } else {
        $control = $("<input>")
            .attr({
                type:"text",
                id:name,
                name:name
            })
            .addClass("edit_input")
            .appendTo($div);
        if (node.data[field]) {
            $control.val(node.data[field]);
        }

    }

    var controls = [$control];
    if ($control2) controls.push($control2);

    _.each(controls,function(control) {
        control.on('change', function (ev) {
            node.data[field] = $(this).val();

            var tree = story_details.$tree.jstree(true);
            var outputNode = story_details.titleNodeFromType(node.data);
            tree.set_text(node, outputNode.text);

            if (outputNode.icon) {
                tree.set_icon(node, outputNode.icon);
            }

            var new_node_pointer = tree.get_node(node);
            if (outputNode.a_attr && outputNode.a_attr.class) {
                new_node_pointer.a_attr = new_node_pointer.a_attr || {};
                new_node_pointer.a_attr.class = new_node_pointer.a_attr.class || "";
                new_node_pointer.a_attr.class += " " + outputNode.a_attr.class;
                new_node_pointer.a_attr.class = _.str.trim(new_node_pointer.a_attr.class);
            }

            tree.deselect_all();
            tree.select_node(node);

            story_details.transformTreeToStory();
        });

        if (schema_item.style) {
            contro.css(schema_item.style);
        }
    });

//        {field: "name", required: true, type: "options-suggested", options_relate_to: "concept", heading: true, default: "magic", options: story_details.suggested.requirement_name},

    return $div;
};
