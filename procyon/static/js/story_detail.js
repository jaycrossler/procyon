var story_details = {};
story_details.MEDIA_PREFIX = "/site_media/media/";
story_details.default_story = {variables: [], story: [], choices: [], requirements: []};
story_details.all_images = {};
story_details.show_parsed_variables = true;
story_details.show_choices_as_tree = true;
story_details.choice_tree_shrink = false;
story_details.new_tree_node_text = "-New added Item-";
story_details.$tree_node_holder = null;
story_details.$tree = null;

story_details.init = function (story) {
    story = story || story_details.default_story;

    //Link all images into the class object
    story_details.all_images = story.images;

    story_details.drawStory(story);
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
        var $tree_node_holder = story_details.$tree_node_holder = $("<div>").appendTo($choices);
        var $tree = $("<div>").appendTo($choices);
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
        .addClass('btn')
        .text("Toggle Tree Editability")
        .on('click', function () {
            story_details.choice_tree_shrink = !story_details.choice_tree_shrink;
            story_details.drawStory();
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
        var new_node = tree.create_node(parent);
        tree.set_text(new_node, text);

        var new_node_pointer = tree.get_node(new_node);
        new_node_pointer.a_attr.class = new_node_pointer.a_attr.class || "";
        new_node_pointer.a_attr.class += " " + type;
        new_node_pointer.a_attr.class = _.str.trim(new_node_pointer.a_attr.class);

        new_node_pointer.state = {opened:"true"};

        if (data) {
            new_node_pointer.data = data;
            tree.edit(new_node, text);
        }
        story_details.showNodeDetail(new_node_pointer, $tree_node_holder);

        return new_node_pointer;
    };
    var preventSubFolders = function (node, parent_type) {
        var type = treeNodeStoryType(node);
        return !nodeIsNotFolder(node)
            || (node.parent == "#")
            || (type == "requirement")
            || (type == "effect")
            || (type == "variable")
            || (node.text == story_details.new_tree_node_text)
            || (type == parent_type);
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
        //TODO: Build a schema, pull these from there
        var data = null;
        if (type == "requirement") {
            data = {concept: "", has: "", exceeds:"", below:"", is:"", name: story_details.new_tree_node_text}
        } else if (type == "choice") {
            data = {title: story_details.new_tree_node_text}
        } else if (type == "chance") {
            data = {title: story_details.new_tree_node_text}
        } else if (type == "effect") {
            data = {function: "functionToRun", variable:"", value:""}
        } else if (type == "variable") {
            data = {name: "story_details.new_tree_node_text", nickname: "item", tags:"", title:"", value:"", subkind:"", details:"", kind:"", strength:"", defense:"", armor:"", weapons:""}
        }
        if (data) data.type = type;
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
        }
    );

};
story_details.showNodeDetail = function (node, $tree_node_holder) {
    $tree_node_holder = $tree_node_holder || story_details.$tree_node_holder;
    var data = node.data || {};
    var variables = [];

    $tree_node_holder.empty();
    if (data && !_.isEmpty(data)) {
        for (key in data) {
            var val = data[key];
            if (!_.isArray(val) && !_.isObject(val)) {
                if (key != "type") variables.push(key);
            }
        }
        _.each(variables, function (field) {
            var val = data[field];
            $("<span>")
                .html("<b>" + field + ":</b> " + val)
                .addClass("field")
                .appendTo($tree_node_holder);
        })

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
    var output = {state: {opened: true}};
    var text = "";
    var children = [];

    if (type == "stories") {
        text = storyItem.name || storyItem.description || "Story";
    } else if (type == "story") {
        text = story_details.nodeTexts.story(storyItem.story);
        //output.icon = ""; //TODO: Set these
    } else if (type == "images") {
        text = story_details.nodeTexts.image(storyItem);
    } else if (type == "chances") {
        //TODO: Incorporate parseInt(100 / num_chances);
        text = story_details.nodeTexts.chance(storyItem);
        output.state = {opened: false};
        output.a_attr = {class: 'chance bold'};
    } else if (type == "effects") {
        text = story_details.nodeTexts.effect(storyItem);
        output.a_attr = {class: 'effect'};
    } else if (type == "requirements") {
        text = story_details.nodeTexts.requirement(storyItem);
        output.a_attr = {class: 'requirement'};
    } else if (type == "variables") {
        text = story_details.nodeTexts.variable(storyItem);
    } else if (type == "choices") {
        text = story_details.nodeTexts.choice(storyItem);
        output.a_attr = {class: 'choice bold'};
    }
    if (story_details.choice_tree_shrink) {
        text = "<b>" + _.str.titleize(type) + "</b>: " + text;
    }
    //For each item, add children if there is a sub-tree
    _.each("story,images,requirements,chances,choices,effects,variables".split(","), function (key) {
        var val = storyItem[key];
        if (val) {
            var node = story_details.convertStoryToTree(val, key);
            if (node) children.push(node);
        }
    });

    if (!text && storyItem.text) {
        text = story_details.text(storyItem.text);
    }

    output.text = _.str.truncate(text || "Unrecognized item", 80);

    if (story_details.choice_tree_shrink) {
        children = _.flatten(children);
    }
    output.children = (children && children.length) ? children : null;
    storyItem.type = type;
    output.data = storyItem;

    return output;
};
story_details.transformTreeToStory = function($tree) {
    $tree = $tree || story_details.$tree;
    var data = $tree.jstree().get_json();

    var json = story_details.exportTreeNode(data);
    var story = json[0].stories[0];

    story_details.default_story = story;
};
story_details.exportTreeNode = function(data) {
    var output = [];
    _.each(data, function (item) {
        var obj = item.data;
        var output_obj = {};
        if (_.isObject(obj) && _.isEmpty(obj) && item.children) {
            var title = item.text.toLowerCase();
            output_obj[title] = story_details.exportTreeNode(item.children);
        } else  if (_.isObject(obj) && item.children) {
            for (key in obj) {
                var val = obj[key];
                if (val && !_.isArray(val) && !_.isObject(val)) {
                    output_obj[key] = obj[key];
                }
            }
        }
        _.each(item.children,function(nodeGroup){
            var title = nodeGroup.text.toLowerCase();
            output_obj[title] = story_details.exportTreeNode(nodeGroup.children);
        });

        if (output_obj){
            output.push(output_obj);
        }
    });
    return output;
};