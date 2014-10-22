var story_details = {};
story_details.MEDIA_PREFIX = "/site_media/media/";
story_details.default_story = {variables: [], story: [], options: [], requirements: []};
story_details.all_images = {};

story_details.init = function (story) {
    //Link all images into the class object
    story_details.all_images = story.images;

    //Draw story complex details
    $("#requirements").append(story_details.buildRequirementsHolder(story.requirements));

    story_details.showVariables(story.variables);
    story_details.showStory(story.story);
    story_details.showOptions(story.options, $("#options"));
    story_details.buildDownloadButtons();
};
story_details.showStory = function (data) {
    var $story = $("#story");
    data = data || [];
    _.each(data, function (story) {
        if (story.text) {
            $("<div>")
                .addClass("story_text")
                .html(story.text)
                .appendTo($story);
        }
        $story.append(story_details.buildImagesHolder(story.images));
    });
};

story_details.showOptions = function (data, $options) {
    //TODO: Make this recursive
    data = data || [];
    _.each(data, function (option) {
        var title = "Option: " + option.title;

        //TODO: Make this a tree
        var $opt = $("<div>")
            .addClass('option')
            .appendTo($options);

        $("<span>")
            .addClass('option_title')
            .html(title)
            .appendTo($opt);

        $opt.append(story_details.buildRequirementsHolder(option.requirements));
        $opt.append(story_details.buildEffectsHolder(option.effects));

        _.each(option.chances || [], function (chance) {
            var $sub_opt = $("<div>")
                .html(" - " + chance.title)
                .addClass("chance")
                .appendTo($opt);

            $sub_opt.append(story_details.buildRequirementsHolder(chance.requirements));
            $sub_opt.append(story_details.buildEffectsHolder(chance.effects));
        });

    });
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
            $var.attr("title", variable.details);
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
        text += "</b>";

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
    $("<a>")
        .addClass('btn download')
        .text("Download Story as JSON")
        .attr('id','download_json_all')
        .on('click',function(){
            var obj = story_details.default_story;
            var data = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));
            window.open(data,'story_'+obj.id);
        })
        .appendTo($('#downloads'));
};