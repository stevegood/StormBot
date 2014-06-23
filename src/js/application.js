var sb = sb || {};

Handlebars.registerHelper('returnIfEqual', function(objVal, expVal, returnVal){
    return objVal === expVal ? returnVal : '';
});

jQuery(function($){

    sb = $.extend({}, sb, {
        settings: {
            player: 'spotify',
            now_playing: {
                save_to_file: true
            },
            twitch: {
                username: 'ThatArdothGuy'
            }
        },
        templates: {},
        init: function() {
            // compile all the handlebars templates
            $('script[type="text/x-handlebars-template"]').each(function(){
                sb.templates[$(this).attr('id')] = Handlebars.compile($(this).html());
            });

            // bind handlers
            $('#music-player-settings-nav').on('click', sb.openMusicPlayerSettings);
            $('#account-settings-nav').on('click', sb.openAccountSettings);
        },

        buildModal: function(templateKey, modalId, obj) {
            if (obj === undefined || obj === null) {
                obj = {};
            }
            var html = sb.templates[templateKey](obj);
            $('body').append(html);
            var $modal = $(modalId);
            $modal.modal({show: true, keyboard: true}).on('hidden.bs.modal', function(){
                $modal.remove();
            });
            return $modal;
        },

        openMusicPlayerSettings: function(event){
            event.preventDefault();
            event.stopPropagation();

            sb.buildModal('music-player-settings-template', '#music-player-settings', sb.settings);
            $('#music-player-save-btn').on('click', sb.saveMusicSettings);
        },

        saveMusicSettings: function() {
            // TODO: save the player settings to a cookie or to local storage some place awesome like that
            sb.settings.player = $('#player-select').val();
            sb.settings.now_playing.save_to_file = $('#save-to-file-cb:checked').length > 0;
            // close the modal window
            $('#music-player-settings').modal('hide');
        },

        openAccountSettings: function(event) {
            event.preventDefault();
            event.stopPropagation();

            sb.buildModal('account-settings-template', '#account-settings', sb.settings);
        }
    });

    sb.init();
});
