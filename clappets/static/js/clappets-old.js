var app_common = {
    data: {
        pageActive: "calcPage",
        errorBoxActive: false,
        error_status: "",
        errors: "",

        msgBoxActive: false,
        message: ""
    },
    computed: {
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
    methods: {
        setActivePage: function(event) {
            this.pageActive = event.target.name;
        },

        get_resource_list: function(resource_name) {
            var app = this;
            app.errorBoxActive = false;
            app.msgBoxActive = false;
            url = app.api_url[resource_name]
            axios.get(url)
                .then(function(response) {
                    resource_list = resource_name + "_list";
                    app[resource_list] = response.data;
                    console.log(response);
                    app.message = "List loaded successfully";
                    app.msgBoxActive = true;
                })
                .catch(function(error) {
                    console.log(error);
                });
        },

        add_resource: function(resource_name) {
            var app = this;
            app.errorBoxActive = false;
            app.errors = {};
            app.error_status = "";
            app.msgBoxActive = false;
            app.message = "";
            url = app.api_url[resource_name];

            axios.post(url, {
                    resource: app[resource_name]
                })
                .then(function(response) {
                    console.log(response);
                    app.message = response.data["_message"];
                    app.msgBoxActive = true;
                })
                .catch(function(error) {
                    console.log(error);
                    app.error_status = error.response.status + " " + error.response.statusText;
                    app.errors = error.response.data
                    app.errorBoxActive = true;
                });
        },

        update_resource: function(resource_name, resource_id) {
            var app = this;
            app.errorBoxActive = false;
            app.errors = {};
            app.error_status = "";
            app.msgBoxActive = false;
            app.message = "";
            url = app.api_url[resource_name] + resource_id + '/'
            axios.put(url, {
                    resource: app[resource_name],
                })
                .then(function(response) {
                    console.log(response);
                    app.message = response.data["_message"];
                    app.msgBoxActive = true;
                })
                .catch(function(error) {
                    console.log(error);
                    app.error_status = error.response.status + " " + error.response.statusText;
                    app.errors = error.response.data
                    app.errorBoxActive = true;
                });
        },

        delete_resource: function(resource_name, resource_id) {
            if (confirm("Want to delete " + resource_id + " in " + resource_name)) {
                var app = this;
                app.errorBoxActive = false;
                app.errors = {};
                app.error_status = "";
                app.msgBoxActive = false;
                app.message = "";
                url = app.api_url[resource_name] + resource_id + '/';
                axios.delete(url)
                    .then(function(response) {
                        console.log(response);
                //        app.get_resource_list(resource_name);
                    location.reload();
                        app.message = "Deletion Successful";
                        app.msgBoxActive = true;
                    })
                    .catch(function(error) {
                        console.log(error);
                        app.error_status = error.response.status + " " + error.response.statusText;
                        app.errors = error.response.data
                        app.errorBoxActive = true;
                    });
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

        hideErrorBox: function() {
            this.errorBoxActive = false;
        },

        hideMsgBox: function() {
            this.msgBoxActive = false;
        },

        print: function() {
            docElement = this.$refs['docWrapper']
            var elems = docElement.getElementsByTagName("input");
            for (var i = 0; i < elems.length; i++) {
                // set attribute to property value
                elems[i].setAttribute("value", elems[i].value);
            }
            console.log(this.$refs['docWrapper'].innerHTML);
        },

        save: function() {
            mydata = JSON.stringify(this.doc, null, 2);
            save_anchor = this.$refs['save_anchor']
            save_anchor.download = "formData-" + new Date().getTime();
            // create a text file
            save_anchor.href = "data:text/plain," + encodeURIComponent(mydata);
            // save `formData` locally as file with timestamp appended to file name
            save_anchor.click();
        },

        load: function() {
            file = this.$refs['fileupload'].files[0];
            var reader = new FileReader();
            var app = this;
            reader.readAsText(file, "UTF-8");
            reader.onload = function(evt) {
                str = evt.target.result;
                doc = JSON.parse(str)
                app.doc = doc
                console.log(doc);
            }
            reader.onerror = function(evt) {
                console.log("error reading file");
            }
        }




    }
};
