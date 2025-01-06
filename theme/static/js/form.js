    import {initializeChart} from './export_chart.js';
    import MAIN_URL from './url.js';
    let modalContent = document.getElementById('modal-content');

    function populateYearSelect(startYear, endYear, element) {
        const currentYear = new Date().getFullYear();
        startYear = startYear || currentYear - 100; // default start year to 100 years ago
        endYear = endYear || currentYear; // default end year to the current year

        for (let year = startYear; year <= endYear; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.text = year;
            element.appendChild(option);
        }
    }
    // 
    document.addEventListener('htmx:afterOnLoad', function(event) {
        let path = event.detail.pathInfo.requestPath
        if (path == '/create-population-projection/'){
            path = path.split('?')[1].split('=')[1].split('&')[0]
            if (path === 'update'){
                document.getElementById('form-header').innerText = 'Update Population Projection'
            }
            else if (path === 'create'){
                document.getElementById('form-header').innerText = 'Create Population Projection'
            }
            else
            {
                document.getElementById('form-header').innerText = ''
            }
        }

        
    });
    // add hidden to modal when request is successful
    modalContent.addEventListener('htmx:afterRequest', (e) => {
        console.log('request successful')
        document.getElementById('my_modal_3').classList.add('hidden')
    })

// handle modal content change DOMContentLoaded
modalContent.addEventListener('htmx:afterSettle', (e) => {
    console.log('modal content changed')
    
    var areaTypeInputs = document.getElementsByName('areaType');
    var regionSelectContainer = document.getElementById('regionSelectContainer');
    var districtSelectContainer = document.getElementById('districtSelectContainer');
    var townSelectContainer = document.getElementById('townSelectContainer');
    var regionSelect = document.getElementById('regionSelect');
    var regionDropdown = document.getElementById('regionDropdown');
    var regionDropdownList = document.getElementById('regionDropdownList');
    var districtSelect = document.getElementById('districtSelect');
    var districtDropdown = document.getElementById('districtDropdown');
    var districtDropdownList = document.getElementById('districtDropdownList');
    var townSelect = document.getElementById('townSelect');
    var townDropdown = document.getElementById('townDropdown');
    var townDropdownList = document.getElementById('townDropdownList');
    var baseYear = document.getElementById('baseYear');
    var projectYear = document.getElementById('projectYear');
    var growthRate = document.getElementById('growthRate');
    var growthRateType = document.getElementById('growthRateType');
    var projectButton = document.getElementById('projectButton');
    const form = document.getElementById('projectionForm');
    var title = document.getElementById('title');
    var description = document.getElementById('description');
    var baseYearPopulation = document.getElementById('baseYearPopulation');
    var loading = document.getElementById('loading');
    var hiddenInput = document.getElementById('hidden')
    var selectedAreaType = document.querySelector('input[name="areaType"]:checked');

    let AreaType = ''
    console.log(loading)
    
    populateYearSelect(1900, null, baseYear);
    populateYearSelect(new Date().getFullYear() - 24, new Date().getFullYear() + 50, projectYear);

    function handleAreaTypeChange(value) {
        if (value === 'region') {
            regionSelectContainer.style.display = 'block';
            districtSelectContainer.style.display = 'none';
            townSelectContainer.style.display = 'none';
            AreaType = 'region'
        } else if (value === 'district') {
            regionSelectContainer.style.display = 'block';
            districtSelectContainer.style.display = 'block';
            townSelectContainer.style.display = 'none';
            AreaType = 'district'
        } else if (value === 'town') {
            regionSelectContainer.style.display = 'block';
            districtSelectContainer.style.display = 'block';
            townSelectContainer.style.display = 'block';
            document.getElementById('growthRateTypeContainer').classList.add('hidden')

            AreaType = 'town'
        }
    }

    
    function slugify (string) {
        const a = 'àáäâèéëêìíïîòóöôùúüûñç';
        const b = 'aaaaeeeeiiiioooouuuunc';
        const p = new RegExp(a.split('').join('|'), 'g');
        return string.toString().toLowerCase()
            .replace(/\s+/g, '-')           // Replace spaces with -
            .replace(p, c => b.charAt(a.indexOf(c))) // Replace special characters
            .replace(/&/g, '-and-')         // Replace & with 'and'
            .replace(/[^\w-]+/g, '')         // Remove all non-word characters
            .replace(/--+/g, '-');           // Replace multiple - with single -
    }
    
    // edit
    let objectId = hiddenInput.value
    if (objectId){
        console.log(objectId)
        let regionData = regionSelect.dataset.value ? regionSelect.dataset.value : '' // get data-value attribute of regionSelect

        let districtData = districtSelect.dataset.value ? districtSelect.dataset.value : '' // get data-value attribute of districtSelect

        let townData = townSelect.dataset.value ? townSelect.dataset.value : '' // get data-value attribute of townSelect

        const initialFormData = new FormData(form);
        // Convert FormData to a plain object
        const initialValues = Object.fromEntries(initialFormData.entries());
        
        let value = selectedAreaType.value
        handleAreaTypeChange(value) // call handleAreaTypeChange function

        
        // handle areaType change
        areaTypeInputs.forEach((input) => {
            input.addEventListener('change', (e) => {
                let value = e.target.value;
                handleAreaTypeChange(value) // call handleAreaTypeChange function
                if (value === 'region') {
                    regionSelect.value = regionData
                } else if (value === 'district') {
                    regionSelect.value = regionData
                    districtSelect.value = districtData
                }
                else if (value === 'town') {

                    regionSelect.value = regionData
                    districtSelect.value = districtData
                    townSelect.value = townData

                    
                }
            })

        })
        

        form.addEventListener('input', function() {
            const currentFormData = new FormData(form);
            const currentValues = Object.fromEntries(currentFormData.entries());
    
            // Check if any field value has changed
            let hasChanged = false;
            for (const key in initialValues) {
                if (initialValues[key] !== currentValues[key]) {
                    hasChanged = true;
                    break;
                }
            }
            let isEmpty = false;
            // loop through currentValues to check if any field is empty except for description
            for (const key in currentValues) {
                if (key !== 'description' && currentValues[key].trim() === '') {
                    isEmpty = true;
                    break;
                }
            }
            if (hasChanged && !isEmpty) {
                projectButton.disabled = false;
            } else {
                projectButton.disabled = true;
            }

        });

        // submit form
        form.addEventListener('submit', (e) => {
            e.preventDefault(); 
            projectButton.innerHTML = `<span id="loading" class="loading loading-spinner loading-md text-gray-600"></span>`
            projectButton.disabled = true;
            
            
            let data = {
                title: title.value,
                description: description.value,
                areaType: selectedAreaType.value,
                region: regionSelect.value,
                district: districtSelect.value,
                town: townSelect.value,
                baseYear: baseYear.value,
                projectYear: projectYear.value,
                baseYearPopulation: baseYearPopulation.value,
                growthRate: growthRate.value,
                growthRateType: growthRateType.value,
                slug: slugify(title.value),
                id: objectId
            }
            console.log(data)
            htmx.ajax('PUT', '/create-population-projection/', {
                historyEventName: 'create-population-projection',
                target: '#main',
                values: data,
                
            })
            .then((response) => {
                // sweet alert
                swal({
                    title: "Success!",
                    text: "Population projection updated successfully!",
                    icon: "success",
                    button: "OK",
                    timer: 3000
                });
                document.getElementById('my_modal_3').close()
            })

        });
            
            
        
    }
    // create
    else{
        // check if selectedAreaType is not empty
       
        let value = selectedAreaType.value
        handleAreaTypeChange(value) // call handleAreaTypeChange function
        
        // handle areaType change
        areaTypeInputs.forEach((input) => {
            input.addEventListener('change', (e) => {
                let value = e.target.value;
                handleAreaTypeChange(value) // call handleAreaTypeChange function
                selectedAreaType = value
                console.log(selectedAreaType)
            })
        })

        // validate form
        function validateForm(){
            const isRegionSelected = regionSelectContainer.classList.contains('hidden') || regionSelect.value.trim() !== '';
            const isDistrictSelected = districtSelectContainer.classList.contains('hidden') || districtSelect.value.trim() !== '';
            const isTownSelected = townSelectContainer.classList.contains('hidden') || townSelect.value.trim() !== '';
            const isBaseYearFilled = baseYear.value.trim() !== '';
            const isProjectYearFilled = projectYear.value.trim() !== '';
            const isGrowthRateFilled = growthRate.value.trim() !== '';
            const isTitleFilled = title.value.trim() !== '';
            const isBaseYearPopulationFilled = baseYearPopulation.value.trim() !== '';
            const isGrowthRateTypeFilled = growthRateType.value.trim() !== '';
            if (isRegionSelected && isDistrictSelected && isTownSelected && isBaseYearFilled && isProjectYearFilled && isTitleFilled && isBaseYearPopulationFilled){
                if(growthRateType.value === 'manual' && isGrowthRateFilled){
                    return true
                }
                else if (growthRateType.value === 'auto' && !isGrowthRateFilled){
                    
                    return true
                }
                else{
                    return false
                }
            }
            else{
                return false
            }
        }

        // handle growthRateType change
        growthRateType.addEventListener('change', function() {
            if (growthRateType.value === 'auto') {
                // hide the growthrate container
                console.log('auto')
                document.getElementById('growthRateContainer').classList.add('hidden')
                growthRate.value = '';
            } else {
                // unhide the growthrate container
                document.getElementById('growthRateContainer').classList.remove('hidden')
            }
            if (validateForm()){
                projectButton.disabled = false;
            } else {
                projectButton.disabled = true;
            }

        });

        // handle input change
        form.addEventListener('input', function() {
            if (validateForm()){
                projectButton.disabled = false;
                
            } else {
                projectButton.disabled = true;
                
            }
        });

        // handle input change
        regionSelect.addEventListener('focus', () => {
            regionDropdown.classList.remove('hidden');
        });

        // handle input change
        regionSelect.addEventListener('input', () => {
            const filter = regionSelect.value.toLowerCase();
            Array.from(regionDropdownList.getElementsByTagName('li')).forEach(option => {
                if (option.textContent.toLowerCase().includes(filter)) {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            });
        });

        regionDropdownList.addEventListener('click', (e) => {
            if (e.target.tagName === 'LI') {
                regionSelect.value = e.target.textContent;
                regionDropdown.classList.add('hidden');
                populateDistricts(e.target.textContent);
            }
        });

        districtSelect.addEventListener('focus', () => {
            districtDropdown.classList.remove('hidden');
        });

        districtSelect.addEventListener('input', () => {
            const filter = districtSelect.value.toLowerCase();
            Array.from(districtDropdownList.getElementsByTagName('li')).forEach(option => {
                if (option.textContent.toLowerCase().includes(filter)) {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            });
        });

        districtDropdownList.addEventListener('click', (e) => {
            if (e.target.tagName === 'LI') {
                districtSelect.value = e.target.textContent;
                districtDropdown.classList.add('hidden');
                populateTowns(e.target.textContent);
            }
        });

        townSelect.addEventListener('focus', () => {
            townDropdown.classList.remove('hidden');
        });

        townSelect.addEventListener('input', () => {
            const filter = townSelect.value.toLowerCase();
            Array.from(townDropdownList.getElementsByTagName('li')).forEach(option => {
                if (option.textContent.toLowerCase().includes(filter)) {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            });
        });

        townDropdownList.addEventListener('click', (e) => {
            if (e.target.tagName === 'LI') {
                townSelect.value = e.target.textContent;
                townDropdown.classList.add('hidden');
                populateTowns(e.target.textContent);  
            }
        });
        window.onload = populateRegions();

        function populateRegions() {
            fetch('http://127.0.0.1:8000/regions',)
                .then(response => response.json())
                .then(data => {
                    const regions = data.regions;
                    
                    regions.forEach(region => {
                        const li = document.createElement('li');
                        li.textContent = region.name;
                        li.className = 'py-3 px-4 rounded-md hover:bg-gray-300 cursor-pointer';
                        regionDropdownList.appendChild(li);
                    });
                });
        }

        function populateDistricts(region) {
            districtDropdownList.innerHTML = '';
            fetch('http://127.0.0.1:8000/districts?region=' + region)
                .then(response => response.json())
                .then(data => {
                    const districts = data.districts;
                    districts.forEach(district => {
                        const li = document.createElement('li');
                        li.textContent = district.name
                        li.className = 'py-3 px-4 rounded-md hover:bg-gray-300 cursor-pointer';
                        districtDropdownList.appendChild(li);
                    });
                });
        }

        function populateTowns(district) {
            townDropdownList.innerHTML = '';
            fetch('http://127.0.0.1:8000/towns?district=' + district)
                .then(response => response.json())
                .then(data => {
                    const towns = data.towns;
                    towns.forEach(town => {
                        const li = document.createElement('li');
                        li.textContent = town.name;
                        li.className = 'py-3 px-4 rounded-md hover:bg-gray-300 cursor-pointer';
                        townDropdownList.appendChild(li);
                    });
                });
        }

        document.addEventListener('click', (event) => {
            if (!regionSelect.contains(event.target) && !regionDropdown.contains(event.target)) {
                regionDropdown.classList.add('hidden');
            }
            if (!districtSelect.contains(event.target) && !districtDropdown.contains(event.target)) {
                districtDropdown.classList.add('hidden');
            }
            if (!townSelect.contains(event.target) && !townDropdown.contains(event.target)) {
                townDropdown.classList.add('hidden');
            }
        });


        // handle form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            // if areaType is region, district or town, check if the region, district and town fields are not empty
            if (selectedAreaType.value === 'region' && regionSelect.value.trim() === '') {
                // make the regionSelect input field required
                regionSelect.required = true;

                return;
                
            }
            if (selectedAreaType.value === 'district' && districtSelect.value.trim() === '') {
                // make regionSelect and districtSelect input fields required
                regionSelect.required = true;
                districtSelect.required = true;
                return;
            }
            if (selectedAreaType.value === 'town' && townSelect.value.trim() === '') {
                // make regionSelect, districtSelect and townSelect input fields required
                regionSelect.required = true;
                districtSelect.required = true;
                townSelect.required = true;
                return;
            }

            projectButton.innerHTML = `
            <span id="loading" class="loading loading-spinner loading-md text-gray-white"></span>
            <span class="ml-2">projecting...</span>
            `
            let data = {
                title: title.value,
                description: description.value,
                areaType: AreaType,
                region: regionSelect.value,
                district: districtSelect.value,
                town: townSelect.value,
                baseYear: baseYear.value,
                projectYear: projectYear.value,
                baseYearPopulation: baseYearPopulation.value,
                growthRate: growthRate.value,
                growthRateType: growthRateType.value,
                slug: slugify(title.value),
            }
            // remove empty values


            console.log(data)

            htmx.ajax('POST', '/create-population-projection/', {
                historyEventName: 'create-population-projection',
                target: '#main',
                values: data,
                
            })
            .then((response) => {
                // sweet alert
                swal({
                    title: "Success!",
                    text: "Population projection created successfully!",
                    icon: "success",
                    button: "OK",
                    timer: 3000
                });
                document.getElementById('my_modal_3').close()
            })
        });    
    

    }


})