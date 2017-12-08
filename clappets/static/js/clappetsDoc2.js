var app_doc = {
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
        errors : {}

        selectionModalisActive: false,
        unitsModalisActive: false,
        infoModalisActive: false,
        saveAsModalisActive: false,
        macroModalisActive: false,
        uploadModalisActive: false,
        selectionMenu: {},
    },
    computed: {
        dimensions_used: function() {
            dimensions = []
            for (var dimension in this.doc.units) {
                if (this.doc.units.hasOwnProperty(dimension)) {
                    dimensions.push(dimension);
                }
            }
            return dimensions;
        },

        doc_id: function() {
            meta = this.doc['meta'];
            id = meta["projectID"] + "-" + meta["discipline"] + "-" + meta["docCategory"] + "-" + meta["docSubCategory"] + "-" + meta["docClass"] + "-" + meta["docInstance"];
            return id;
        }
    },
    methods: {
        gUL: function(dimension) {
            try {
                unitUsed = this.doc.units[dimension]
                unitLabel = getUnitLabel(dimension, unitUsed)
                return unitLabel
            } catch (err) {
                console.log("Error occured in getUnitLabel trying to fetch unitUsed '" + unitUsed + "'")
                return '';
            }
        },

        getUnits: function(dimension) {
            try {
                return getUnits(dimension)
            } catch (err) {
                console.log("Error occured in getUnits with dimension = '" + dimension + "'");
            }
        },

        getErrs: function(path_array) {
            val = this.errors
            try {
                for (var key of path_array) {
                    val = val[key]
                }
                return val
            } catch (err) {
                return []
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

        calculate: function() {
            alert("you ran the calculation");
        },

        newDoc: function() {
            this.execQuery("/api/document/tpl/");
            app.selectionModalisActive = true;
        },

        saveDoc: function() {
            mydata = JSON.stringify(this.doc, null, 2);
            save_anchor = this.$refs['save_anchor']
            save_anchor.download = "formData-" + new Date().getTime();
            save_anchor.href = "data:text/plain," + encodeURIComponent(mydata);
            save_anchor.click();
        },

        openDocDB: function() {
            this.execQuery("/api/document/query/");
            app.selectionModalisActive = true;
        },

        saveDocDB: function() {
            var app = this;
            this.resetMessages();
            if (this.doc['_id'] == "") {
                this.saveAsModalisActive = true;
            } else {
                url = "/api/document/db/" + this.doc["_id"] + "/";
                axios.put(url, {
                        doc: app.doc
                    })
                    .then(function(response) {
                        console.log(response);
                        app.successMessage = response.data["message"];
                        app.successisActive = true;
                    })
                    .catch(function(error) {
                        console.log(error);
                        app.errorStatus = error.response.status + " " + error.response.statusText;
                        app.errors = error.response.data
                        app.errorisActive = true;
                    });
            }
        },

        saveAsDocDB: function() {
            this.saveAsModalisActive = false;
            var app = this;
            this.resetMessages()
            url = "/api/document/db/"
            axios.post(url, {
                    doc: app.doc
                })
                .then(function(response) {
                    console.log(response);
                    alert("Document Successfully Saved. Now reloading")
                    location.href = "/htm/document/db/" + response.data["_id"] + "/";
                    //app.doc["_id"] = response.data["_id"];
                    app.successMessage = response.data["message"];
                    app.successisActive = true;
                })
                .catch(function(error) {
                    console.log(error);
                    app.errorStatus = error.response.status + " " + error.response.statusText;
                    app.errors = error.response.data
                    app.errorisActive = true;
                });
        },

        deleteDocDB: function() {
            var app = this;
            this.resetMessages();
            if (this.doc['_id'] == "") {
                alert("Document does not have a valid ID");
                return;
            } else {
                url = "/api/document/db/" + this.doc["_id"] + "/";
                axios.delete(url)
                    .then(function(response) {
                        console.log(response);
                        location.href = "/htm/document/"
                    })
                    .catch(function(error) {
                        console.log(error);
                        app.errorStatus = error.response.status + " " + error.response.statusText;
                        app.errors = error.response.data
                        app.errorisActive = true;
                    });
            }
        },

        print: function() {
            window.print();
        },

        pdf_download: function() {
            var app = this;
            axios({
                    method: 'post',
                    url: '/pdf/document/',
                    responseType: 'arraybuffer',
                    data: {
                        doc: app.doc
                    }
                })
                .then(function(response) {
                    let blob = new Blob([response.data], {
                        type: 'application/pdf'
                    });
                    let link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'PDF Report.pdf';
                    link.click();
                });
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


    },//end of methods

    beforeMount : function(){
        this.username = localStorage["username"];
        if (localStorage["userAuthenticated"]=="true"){
            this.userAuthenticated = true;
        }
        else{
            this.userAuthenticated = false;
        }

    }
}
