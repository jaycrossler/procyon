var story_details = {};
story_details.MEDIA_PREFIX = "/site_media/media/";
story_details.default_story = {variables: [], story: [], options: [], requirements: []};
story_details.all_images = {};
story_details.show_parsed_variables = true;

story_details.init = function (story) {
    story = story || story_details.default_story;

    //Link all images into the class object
    story_details.all_images = story.images;

    story_details.drawStory(story);
};
story_details.drawStory = function(story) {
    story = story || story_details.default_story;
    //Draw story complex details
    $("#requirements, #story, #options, #variables, #downloads").empty();

    $("#requirements").append(story_details.buildRequirementsHolder(story.requirements));
    $("#options").append(story_details.buildOptions(story.options));

    story_details.showVariables(story.variables);
    story_details.showStory(story.story);
    story_details.buildDownloadButtons();
};
story_details.showStory = function (data) {
    var $story = $("#story");
    data = data || [];
    _.each(data, function (story) {
        if (story.text) {
            $("<div>")
                .addClass("story_text")
                .html(story_details.text(story.text))
                .appendTo($story);
        }
        $story.append(story_details.buildImagesHolder(story.images));
    });
};

//TODO: Make this a tree using a library
story_details.buildOptions = function (options) {
    var $holder = $("<div>");

    _.each(options || [], function (option) {
        var $opt = $("<div>")
            .addClass('option')
            .appendTo($holder);

        var title = "Player Option: <b>" + story_details.text(option.title)+"</b>";
        $("<span>")
            .addClass('option_title')
            .html(title)
            .appendTo($opt);

        $opt.append(story_details.buildRequirementsHolder(option.requirements));
        $opt.append(story_details.buildEffectsHolder(option.effects));

        var chances = option.chances || [];
        var num_chances = chances.length;
        //TODO: Loop through each and find total probability

        _.each(chances, function (chance) {
            var percent = parseInt(100/num_chances);
            var $sub_opt = $("<div>")
                .html(percent+"% : " + story_details.text(chance.title))
                .addClass("chance")
                .appendTo($opt);

            $sub_opt.append(story_details.buildRequirementsHolder(chance.requirements));
            $sub_opt.append(story_details.buildEffectsHolder(chance.effects));

            if (chance.options) {
                $sub_opt.append(story_details.buildOptions(chance.options));
            }
        });

    });
    return $holder;
};
story_details.showVariables = function (data) {
    var $vars = $("#variables");
    data = data || [];
    _.each(data, function (variable) {
        var header = "<b>Variable: [" + variable.nickname + "]</b>: " + variable.name + ", Type: <b>" + variable.type+"</b>";
        if (variable.subtype) {
            header += " (" + variable.subtype + ")"
        }
        if (variable.tags) {
            header += " (" + variable.tags + ")"
        }

        var $var = $("<div>")
            .html(header)
            .appendTo($vars);

        if (variable.details) {
            $var
                .css("cursor","hand")
                .attr("title", variable.details);
        }

    });
};

// --- HTML Holder Builders
story_details.buildEffectsHolder = function (effects) {
    var $effects_holder = $("<span>");
    _.each(effects, function (effect) {
        var text = "<b>" + effect.function;
        if (effect.value) {
            text += "(" + effect.value + ")";
        }
        if (effect.variable) {
            text += "(" + story_details.text(effect.variable) + ")";
        }
        text += "</b> ";
        $("<span>")
            .html(text)
            .addClass('effect')
            .appendTo($effects_holder);
    });
    return $effects_holder;
};

story_details.buildRequirementsHolder = function (data) {
    var $holder = $("<span>");
    data = data || [];
    _.each(data, function (requirement) {
        var text = "<b>" + requirement.concept + "." + requirement.name;
        if (requirement.has) {
            text += " has a value in it of " + requirement.has;
        } else if (requirement.exceeds) {
            text += " >= " + requirement.exceeds;
        } else if (requirement.below) {
            text += " <= " + requirement.below;
        } else if (requirement.is) {
            text += " = " + requirement.is;
        } else if (requirement.isnt) {
            text += " is not = " + requirement.isnt;
        } else {
            text += " is set and isn't 0";
        }
        text += "</b> ";

        $("<span>")
            .addClass('requirement')
            .attr('title',"Requires")
            .html(text)
            .appendTo($holder);
    });
    return $holder;
};

story_details.buildImagesHolder = function (data) {
    var $holder = $("<span>");
    _.each(data, function (image) {
        var allImages = story_details.all_images;
        var url = null;
        _.each(allImages, function (imageLookup) {
            if (_.isString(imageLookup) && _.str.startsWith(imageLookup, "http")) {
                url = imageLookup;
            } else if (_.str.startsWith(imageLookup.url, "http")) {
                url = imageLookup.url;
            } else if (imageLookup.url.indexOf(image.url) > 0) {
                url = story_details.MEDIA_PREFIX + imageLookup.url;
            }
        });

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
        .attr('id','download_json_all')
        .on('click',function(){
            var obj = story_details.default_story;
            var data = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));
            window.open(data,'story_'+obj.id);
        })
        .appendTo($downloads);

    $("<a>")
        .addClass('btn')
        .text("Toggle Parsed Variables")
        .attr('id','download_json_all')
        .on('click',function(){
            story_details.show_parsed_variables = !story_details.show_parsed_variables;
            story_details.drawStory();
        })
        .appendTo($downloads);

};

story_details.text = function(text){
    return (story_details.show_parsed_variables ? story_details.replaceParsedVariables(text) : text);
};
story_details.replaceParsedVariables = function(text,variables){
    variables = variables || story_details.default_story.variables;

    //Look for variables in text. If found, loop through each and replace them in text
    var var_finder = new RegExp("\[[\\w:]+\]", "ig");
    var matches = var_finder.exec(text);
    if (matches && matches.length) {
        _.each(matches, function(match){
            _.each(variables,function(v){
                if (v.nickname && match.indexOf(v.nickname)>0 && text.indexOf("["+ v.nickname)>-1) {
                    //This is the variable described

                    var var_finder = new RegExp("\\["+ v.nickname+"\\]", "ig");
                    text = text.replace(var_finder, "<b>" + v.nickname + "</b>");

                    _.each('name tags value subtype type details'.split(" "),function(field){
                        if (v[field]) {
                            var var_finder = new RegExp("\\["+ v.nickname+":"+field+"\\]", "ig");
                            text = text.replace(var_finder, "<b>" + v[field] + "</b>");
                        }

                    });
                }
            });
        })
    }

    return text;
};