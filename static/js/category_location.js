var StateDistrictInfo = {
    "Karnataka": {
        "Bagalkot": {
            "Los Angeles": ["90001", "90002", "90003", "90004"],
            "San Diego": ["92093", "92101"]
        },

        "Chitradurga": {
            "Chitradurga": ["577501", "577502", "577503", "577504","577505", "577510", "577515", "577525"],
            "Challakere": ["577501", "577502", "577503", "577504","577505", "577510", "577515", "577525"]
            }
    },
    "TamilNadu": {
        "Chennai": {
            "Dispur": ["781005"],
            "Guwahati": ["781030", "781030"]
        },
        "Madurai": {
            "Vadodara": ["390011", "390020"],
            "Surat": ["395006", "395002"]
        }
    }
}

window.onload = function () {

    //Get html elements
    var stateSel = document.getElementById("stateSel");
    var districtSel = document.getElementById("districtSel");
    var citySel = document.getElementById("citySel");
    var zipSel = document.getElementById("zipSel");

    //Load countries
    for (var state in StateDistrictInfo) {
        stateSel.options[stateSel.options.length] = new Option(state, state);
    }

    //County Changed
    stateSel.onchange = function () {

        districtSel.length = 1; // remove all options bar first
        citySel.length = 1; // remove all options bar first
        zipSel.length = 1; // remove all options bar first

        if (this.selectedIndex < 1)
            return; // done

        for (var district in StateDistrictInfo[this.value]) {
            districtSel.options[districtSel.options.length] = new Option(district, district);
        }
    }

    //State Changed
    districtSel.onchange = function () {

        citySel.length = 1; // remove all options bar first
        zipSel.length = 1; // remove all options bar first

        if (this.selectedIndex < 1)
            return; // done

        for (var city in StateDistrictInfo[stateSel.value][this.value]) {
            citySel.options[citySel.options.length] = new Option(city, city);
        }
    }

    //City Changed
    citySel.onchange = function () {
        zipSel.length = 1; // remove all options bar first

        if (this.selectedIndex < 1)
            return; // done

        var zips = StateDistrictInfo[stateSel.value][districtSel.value][this.value];
        for (var i = 0; i < zips.length; i++) {
            zipSel.options[zipSel.options.length] = new Option(zips[i], zips[i]);
        }
    }

}
