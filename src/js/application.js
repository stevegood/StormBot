var sb = sb || {};

Handlebars.registerHelper('returnIfEqual', function(objVal, expVal, returnVal){
    return objVal === expVal ? returnVal : '';
});

Handlebars.registerHelper('returnIfNotEqual', function(objVal, expVal, returnVal){
    return objVal !== expVal ? returnVal : '';
});

jQuery(function($){

    sb = $.extend({}, sb, {
        settings: {
            player: 'spotify',
            now_playing: {
                save_to_file: true
            },
            twitch: {
                api: 'https://api.twitch.tv/kraken',
                username: '',
                oauth: '',
                status: {},
                stream: {
                    status: '',
                    game: ''
                },
                clientid: 'q7uafc0om8r3r7h8m73m43sxo37ujc2'
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
            $('#dashboard-nav').on('click', sb.openDashboard);

            sb.loadSettings();
        },

        loadSettings: function() {
            if (localStorage !== undefined) {
                sb.settings = $.extend({}, sb.settings, JSON.parse(localStorage.getItem('sb.settings')));
            }

            initSettings(sb.settings);
            //sb.initTwitch();
            sb.loadChat();
        },

        saveSettings: function() {
            if (localStorage !== undefined) {
                localStorage.setItem('sb.settings', JSON.stringify(sb.settings));
            }
        },

        initTwitch: function() {
            var scope = [
                    'user_read',
                    'channel_read',
                    'channel_editor',
                    'channel_subscriptions',
                    'user_subscriptions',
                    'channel_check_subscription',
                    'chat_login'
                ],
                redirect_url = 'http://stormblessedlegion.com/stormBot/authorize',
                url = "https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=" + sb.settings.twitch.clientid + "&redirect_uri=" + redirect_url + "&scope=" + scope.join(' ');
            console.log(url);
            var w = window.open(url, "Authorize StormBot", "width=450, height=750");
            w.addEventListener('success', function(event) {
                w.close();
                console.log(event.code);
                Twitch.init({clientId: sb.settings.twitch.clientid}, function(error, status){
                    Twitch.api({method: ''})
                    sb.getStreamInfo();
                });
            });
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

        loadChat: function() {
            if (sb.settings.twitch.username.length) {
                var html = sb.templates['chat-iframe-template'](sb.settings.twitch);
                $('#chat').html(html);
            } else {
                sb.openAccountSettings();
            }
        },

        openMusicPlayerSettings: function(event){
            event.preventDefault();
            event.stopPropagation();

            sb.buildModal('music-player-settings-template', '#music-player-settings', sb.settings);
            $('#music-player-save-btn').on('click', sb.saveMusicSettings);
        },

        saveMusicSettings: function() {
            // save the player settings to a cookie or to local storage some place awesome like that
            sb.settings.player = $('#player-select').val();
            sb.settings.now_playing.save_to_file = $('#save-to-file-cb:checked').length > 0;
            // close the modal window
            $('#music-player-settings').modal('hide');
            setMusicPlayer(sb.settings.player, sb.settings.now_playing.save_to_file);
            sb.saveSettings();
        },

        openAccountSettings: function(event) {
            if (event !== undefined) {
                event.preventDefault();
                event.stopPropagation();
            }

            var $modal = sb.buildModal('account-settings-template', '#account-settings', sb.settings);
            $('#account-settings-save-btn').on('click', function(){
                var username = $('#username-field').val().trim();
                if (!username.length) {
                    alert('A username is required');
                    return;
                }

                sb.settings.twitch.username = username;
                sb.saveSettings();
                sb.loadChat();
                $modal.modal('hide');
            });
        },

        openDashboard: function(event) {
            if (event !== undefined) {
                event.preventDefault();
                event.stopPropagation();
            }

            sb.buildModal('stream-dashboard-template', '#stream-dashboard', sb.settings);
            sb.getStreamInfo();
            $('#vod_form').on('submit', sb.updateFormSubmit);
        },

        getStreamInfo: function() {
            Twitch.api({method: 'channel'}, function(error, channel){
                sb.settings.twitch.stream.status = channel.status;
                sb.settings.twitch.stream.game = channel.game;
            });
//            $.getJSON(sb.settings.twitch.api + '/streams/' + sb.settings.twitch.username,{callback: '?'}, function(resp) {
//                sb.settings.twitch.stream.status = resp.stream.channel.status;
//                sb.settings.twitch.stream.game = resp.stream.channel.game;
//            });
        },

        updateFormSubmit: function(event) {
            event.preventDefault();
            event.stopPropagation();
            var $this = $(this),
                action = $this.attr('action'),
                status = $('#vod_status').val(),
                game = $('#gameselector_input').val();

            $.ajax({
                type: 'PUT',
                url: sb.settings.twitch.api + '/channels/' + sb.settings.twitch.username + '/',
                data: {
                    channel: {
                        status: status,
                        game: game
                    }
                },
                success: function (resp) {
                    // TODO: show an alert or something
                },
                error: function(xhr, status, e) {
                    console.log("Failed!");
                    console.log(status);
                    console.log(e);
                }
            });

            return false;
        }
    });

    sb.init();
});
