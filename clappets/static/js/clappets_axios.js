var app_common = {
    data: {
        userAuthenticated : false,
        username: '',
        password: '',
        loginModalisActive : false,
        successMessage: "",
        successisActive: false,
        warningMessage: "",
        warningisActive: false,
        errorMessage: "",
        errorisActive: false,
        errorStatus:"",
        errors : {},
        selectionMenu: {},

    },
    computed : {
        isReadonly: function() {
            if (this.action == "view") {
                return true;
            } else {
                return false;
            }
        },

        id_isReadonly: function() {
            if ((this.action == "edit") || (this.action == "view")) {
                return true;
            } else {
                return false;
            }
        }
    },





    methods : {
        getErrs: function(path_array) {
            val = this.errors;
            try {
//                for (var key of path_array) {
//                    val = val[key];
//                }
//                return val;
                return [];
            } catch (err) {
                return [];
            }
        },

        openModal: function(modalisActive) {
            this[modalisActive] = true;
            this.resetMessages();
        },

        closeModal: function(modalisActive) {
            this[modalisActive] = false;
            this.resetMessages();
        },

        hideWarning: function() {
            this.warningisActive = false;
        },

        hideError: function() {
            this.errorisActive = false;
        },

        hideSuccess: function() {
            this.successisActive = false;
        },

        resetMessages: function() {
            this.warningMessage = "";
            this.successMessage = "";
            this.errorStatus = "";
            this.errorMessage = "";
            this.errors = {};
            this.errorisActive = false;
            this.warningisActive = false;
            this.successisActive = false;
        },

        login: function(){
            var app = this;
            app.resetMessages();
            axios({
                  method:'post',
                  url:'/auth/',
                  data: {
                      username : app.username,
                      password : app.password
                  }
                })
                .then(function(response) {
                    console.log(response.data);
                    app.userAuthenticated = true;
                    localStorage.setItem('access_token', response.data['access_token']);
                    // use the token received to perform a basic authentication on login test. Browser will rememeber the Credentials
                    // for all future requests and dispatch tokens automatically.
                    url = "/login-test/";
                    token = localStorage["access_token"];
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", url, true, token, "unused");
                    xhr.onload = function (e) {
                      if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            localStorage.setItem('username', app.username);
                            localStorage.setItem('userAuthenticated', app.userAuthenticated);
                            app.successMessage = "User Successfully Logged In"
                            app.successisActive = true;
                            app.loginModalisActive = false;

                        } else {
                          console.error(xhr.statusText);
                          app.errorMessage = "Login Failed.";
                          app.errorisActive = true;
                        }
                      }
                    };
                    xhr.onerror = function (e) {
                      console.error(xhr.statusText);
                      app.errorMessage = "Login Failed.";
                      app.errorisActive = true;
                    };
                    xhr.send(null);
                })
                .catch(function(error) {
                    app.userAuthenticated = false;
                    localStorage.setItem('access_token', 'junk');
                    localStorage.setItem('username', app.username);
                    localStorage.setItem('userAuthenticated', app.userAuthenticated);
                    console.log(error);
                    app.errorStatus = error.response.status + " " + error.response.statusText;
                    app.errors = error.response.data;
                    app.errorMessage = app.getErrs(['message']);
                    app.errorisActive = true;
                });
        },


        logout: function(){
            var app = this;
            app.resetMessages();
            localStorage.setItem('access_token', 'junk');
            localStorage.setItem('username', '');
            localStorage.setItem('userAuthenticated', false);
            token = localStorage["access_token"];
            app.username = localStorage["username"];
            if (localStorage["userAuthenticated"]=="true"){
                app.userAuthenticated = true;
            }
            else{
                app.userAuthenticated = false;
            }
            url = "/login-test/"
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true, token, "unused");
            xhr.onload = function (e) {
              if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    app.errorMessage = "Failed to Logout"
                    app.errorisActive = true;
                } else {
                  console.error(xhr.statusText);
                  app.successMessage = "User successfully logged out";
                  app.successisActive = true;
                  location.href = "/index";
                }
              }
            };

            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(null);
        },

        loadProtectedResource: function(url){
            token = localStorage["access_token"];
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true, token, "unused");
            xhr.onload = function (e) {
              if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    console.log(xhr.responseText);
                    document.location.pathname = url;
                } else {
                    app.errorMessage = xhr.statusText;
                    app.errorisActive = true;
                    console.error(xhr.statusText);
                }
              }
            };
            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(null);
        }, //end of loadProtectedResource

        get_resource_list: function(resource_name) {
            var app = this;
            this.resetMessages();
            url = app.api_url[resource_name]
            axios.get(url)
                .then(function(response) {
                    console.log(response);
                    resource_list = resource_name + "_list";
                    app[resource_list] = response.data;
                })
                .catch(function(error) {
                    console.log(error);
                    app.errorStatus = error.response.status + " " + error.response.statusText;
                    app.errorMessage = error.response.data["message"];
                    app.errors = error.response.data;
                    app.errorisActive = true;
                });
        },

        get_resource: function(resource_name, resource_id) {
            var app = this;
            this.resetMessages();
            url = app.api_url[resource_name] + resource_id + "/"
            axios.get(url)
                .then(function(response) {
                    app[resource_name] = response.data;
                    console.log(response);
                })
                .catch(function(error) {
                    console.log(error);
                    app.errorStatus = error.response.status + " " + error.response.statusText;
                    app.errorMessage = error.response.data["message"];
                    app.errors = error.response.data;
                    app.errorisActive = true;
                });
        },

        add_resource: function(resource_name) {
            var app = this;
            this.resetMessages();
            url = app.api_url[resource_name];
            axios.post(url, {
                    resource: app[resource_name]
                })
                .then(function(response) {
                    console.log(response);
                    app.successMessage = response.data["message"];
                    app.successisActive = true;
                    if (response.data.hasOwnProperty("redirect_url")){
                        location.href = response.data["redirect_url"];
                    }
                })
                .catch(function(error) {
                    console.log(error);
                    app.errorStatus = error.response.status + " " + error.response.statusText;
                    app.errorMessage = error.response.data["message"];
                    app.errors = error.response.data;
                    app.errorisActive = true;
                });
        },

        update_resource: function(resource_name, resource_id) {
            var app = this;
            this.resetMessages();
            url = app.api_url[resource_name] + resource_id + '/'
            axios.put(url, {
                    resource: app[resource_name],
                })
                .then(function(response) {
                    console.log(response);
                    app.successMessage = response.data["message"];
                    app.successisActive = true;
                })
                .catch(function(error) {
                    console.log(error);
                    app.errorStatus = error.response.status + " " + error.response.statusText;
                    app.errorMessage = error.response.data["message"];
                    app.errors = error.response.data;
                    app.errorisActive = true;
                });
        },

        delete_resource: function(resource_name, resource_id) {
            if (confirm("Want to delete " + resource_id + " in " + resource_name)) {
                var app = this;
                this.resetMessages();
                url = app.api_url[resource_name] + resource_id + '/';
                axios.delete(url)
                    .then(function(response) {
                        console.log(response);
                        app.successMessage = response.data["message"];
                        app.successisActive = true;
                        if (response.data.hasOwnProperty("redirect_url")){
                            location.href = response.data["redirect_url"];
                        }
                    })
                    .catch(function(error) {
                        console.log(error);
                        app.errorStatus = error.response.status + " " + error.response.statusText;
                        app.errorMessage = error.response.data["message"];
                        app.errors = error.response.data;
                        app.errorisActive = true;
                    });
            }
        },

        handle_success : function(response){
            console.log(response);
            this.successMessage = response.data["message"];
            this.successisActive = true;
            if (response.data.hasOwnProperty("redirect_url")){
                location.href = response.data["redirect_url"];
            }
        },

        handle_errors : function(error){
            console.log(error);
            app.errorStatus = error.response.status + " " + error.response.statusText;
            app.errorMessage = error.response.data["message"];
            app.errors = error.response.data;
            app.errorisActive = true;
        },

        execQuery: function(query_url) {
            if (query_url.substring(0, 4) == "/api") {
                var app = this;
                url = query_url;
                axios({
                      method:'get',
                      url:query_url,
                    })
                    .then(function(response) {
                        app.selectionMenu = response.data;
                        console.log(response);
                    })
                    .catch(function(error) {
                        console.log(error);
                        app.errorMessage = error.response.data;
                    });
            } else if (query_url.substring(0, 4) == "/htm") {
                location.href = query_url;
            }
        },

        print: function() {
            window.print();
        },

        pdf_download: function(resource_name) {
            var app = this;
            axios({
                    method: 'post',
                    url : app.pdf_url[resource_name],
                    responseType: 'arraybuffer',
                    data: {
                        resource : app[resource_name]
                    }
                })
                .then(function(response) {
                    var blob = new Blob([response.data], {
                        type: 'application/pdf'
                    });
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'PDF Report.pdf';
                    link.click();
                });
        },
    },

    beforeMount : function(){
        try{
            this.username = localStorage.getItem("username");
            if (localStorage.getItem("userAuthenticated")=="true"){
                this.userAuthenticated = true;
            }
            else{
                this.userAuthenticated = false;
            }
        }catch(e){
            this.username = "";
            this.userAuthenticated = false;
        }

        if (this.username=='null'){
            this.username = "";
        }
    }
}
