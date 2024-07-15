import { innerHTMLListener } from "./innerHTMLListener.js";

document.addEventListener('htmx:afterSettle', function(e) {
    console.log(e.detail.target.id)
    if (e.detail.target.id === 'main'){
        // check url to determine if it is the needs assessment page with the regrex of '/needs-assessment/[a-zA-Z0-9]' or '/needs-assessment/' 
        let url = window.location.pathname;

        if (url === '/needs-assessment/' || url.includes('edit')){
            console.log('needs assessment page')
            main()
        }
        
    }
  
})

// page reload
document.addEventListener('DOMContentLoaded', function() {
    // check url to determine if it is the needs assessment page with the regrex of '/needs-assessment/[a-zA-Z0-9]' or '/needs-assessment/'
    let url = window.location.pathname
    if (url === '/needs-assessment/' || url.includes('edit')){
        main()
        console.log('needs assessment page')
    }

})







// function to handle needs assessment page
function main(){
        let sectorSelection = document.getElementById('sectorSelection');
        let healthTypeContainer = document.getElementById('healthTypeContainer');
        let needsAssessmentBtn = document.getElementById('needsAssessmentBtn');
        let projectedPopulationSelect = document.getElementById('projectedPopulationSelect');
        let sectorType = document.getElementById('sectorType');
        const facilityCheckboxes = document.querySelectorAll('.facility-checkbox');
        const facilityNumbersContainer = document.getElementById('facilityNumbers');
        const facilityNumbersContainerMain = document.getElementById('facilityNumberContainer');
    
        let healthFacilityTypeContainer = document.getElementById('healthFacilityTypeContainer');
        let needsAssessmentSlug = document.getElementById('needs_assessment_slug')
        let needsAssessmentSector = document.getElementById('needs_assessment_sector')
        let needType = document.getElementById('need_type')
        
        let healthContainer = document.getElementById('health')

        let personnelCheckboxes = document.querySelectorAll('.personnel-checkbox');

        let personnelNumberContainerMain = document.getElementById('personnelNumberContainer')


        let healthPersonnel = document.getElementById('healthPersonnel')
        let healthFacility = document.getElementById('healthFacility')
    

        // check if post or put request
        let url = window.location.pathname
       
        let postRequest = false;

        if (url === '/needs-assessment/'){
            postRequest = true;
        }
        console.log(url, postRequest)

        if (postRequest){
            console.log('POST')
            let sectorSelectionValue = sectorSelection.value;
            if (sectorSelectionValue === 'health'){
                healthTypeContainer.classList.remove('hidden');
                healthContainer.classList.remove('hidden')
            
            } else {
                healthTypeContainer.classList.add('hidden');
                healthContainer.classList.add('hidden')
                
            }
            // check the value of the health type dropdown
            let type = sectorType.value;
            if (type === 'facility'){
                healthFacility.classList.remove('hidden');
                healthPersonnel.classList.add('hidden');
               
            } else {
                healthFacility.classList.add('hidden');
                healthPersonnel.classList.remove('hidden');
            }

            // add event listener to sector selection dropdown
            sectorSelection.addEventListener('change', function(){
                let sectorSelectionValue = sectorSelection.value;
                if (sectorSelectionValue === 'health'){
                    healthTypeContainer.classList.remove('hidden');
                    healthContainer.classList.remove('hidden')
                    handleCheckboxChange()
                } else {
                    healthTypeContainer.classList.add('hidden');
                    healthContainer.classList.add('hidden')
                    handleCheckboxChange()
                }
            })

            // add event listener to health type dropdown
            sectorType.addEventListener('change', function(){
                let healthTypeValue = sectorType.value;
                if (healthTypeValue === 'facility'){
                    healthFacility.classList.remove('hidden');
                    healthPersonnel.classList.add('hidden');
                    handleCheckboxChange()
                    
                } else {
                    healthFacility.classList.add('hidden');
                    healthPersonnel.classList.remove('hidden');
                    handleCheckboxChange()
                }
            })

            handleCheckboxChange()

            // add event listener to projected population select

            // handle checkbox change if type is facility or personnel
            function handleCheckboxChange(){
                if (sectorType.value === 'facility') {
                    // if facilityNumberContainer is not empty, disable the needs assessment button
                    let inputs = facilityNumbersContainerMain.querySelectorAll('input');
                    let isEmpty = checkEmptyInput(inputs);
                    needsAssessmentBtn.disabled = isEmpty;
                    console.log(isEmpty)
                    
                    // add event listener to facility checkboxes
                    
                    facilityCheckboxes.forEach((checkbox, index) => {
                        checkbox.addEventListener('change', function(e) {
                            let facilityType = e.target.value;
                            const inputFieldId = `${facilityType}`;
                            facilityType = facilityType.charAt(0).toUpperCase() + facilityType.slice(1);
                
                            let inputField = document.createElement('div');
                            inputField.id = inputFieldId;
                
                            if (e.target.checked) {
                                inputField.innerHTML = `
                                    <div class="form-control">
                                        <span class="label-text mb-2">${facilityType}
                                            <p class="italic" style="font-style:italic">(enter number of ${facilityType}s)</p>
                                        
                                        <input id=${facilityType.replace(' ', '')} value="" type="number" min="1" name="facilityNumber-${facilityType}" class="input mt-2 input-bordered w-full" />
                                    </div>
                                `;
                                // Remove the corresponding skeleton
                                const skeleton = document.querySelector(`#skeleton-${index}`);

                                if (skeleton) {
                                    skeleton.remove();
                                }

                                facilityNumbersContainer.appendChild(inputField);
                            } else {
                                const existingInputField = document.getElementById(inputFieldId);
                                if (existingInputField) {
                                    existingInputField.remove();
                                    
                                    // Re-add the corresponding skeleton
                                    let skeleton = document.createElement('div');
                                    skeleton.id = `skeleton-${index}`;
                                    skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                                    skeleton.innerHTML = `
                                        <span class="label-text mb-2">
                                            <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                            <p class="italic">
                                                <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                            </p>
                                        </span>
                                        <div class="h-10 bg-gray-300 rounded w-full"></div>
                                    `;
                                    
                                    facilityNumbersContainer.appendChild(skeleton);
                                }
                            }
                            let newInputs = facilityNumbersContainerMain.querySelectorAll('input');
                            let isEmpty = checkEmptyInput(newInputs); // check if input field is empty
                            
                            needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button

                            // add event listener to input fields to check if they are empty
                            console.log(newInputs)
                            newInputs.forEach(input =>{
                                input.addEventListener('input', function(){
                                    // check all input fields to see if they are empty
                                    let isEmpty = checkEmptyInput(newInputs);
                                    needsAssessmentBtn.disabled = isEmpty;
                                })
                            })
                        });

                        
                    });

                    
                }
                
                else{   
                    let inputs = personnelNumberContainerMain.querySelectorAll('input');
                    let isEmpty = checkEmptyInput(inputs);
                    needsAssessmentBtn.disabled = isEmpty;
                    console.log(isEmpty)
                    personnelCheckboxes.forEach((checkbox, index) => {
                        checkbox.addEventListener('change', function(e) {
                            let personnelType = e.target.value;
                            const inputFieldId = `${personnelType}`;
                            personnelType = personnelType.charAt(0).toUpperCase() + personnelType.slice(1);
                            
                
                            let inputField =  document.createElement('div');
                            inputField.id = inputFieldId;
                
                            if (e.target.checked) {
                                inputField.innerHTML = `
                                    <div class="form-control">
                                        <span class="label-text mb-2">${personnelType}
                                            <p class="italic" style="font-style:italic">(enter number of ${personnelType}s)</p>

                                        <input id=${personnelType} value="" type="number" min="1" name="personnelNumber-${personnelType}" class="input mt-2 input-bordered w-full" />
                                    </div>
                                `;
                                // Remove the corresponding skeleton
                                const skeleton = personnelNumbers.querySelector(`#skeleton-${index}`);

                                if (skeleton) {
                                    skeleton.remove();
                                }

                                personnelNumbers.appendChild(inputField);
                            } 
                            else {
                                const existingInputField = document.getElementById(inputFieldId);
                                if (existingInputField) {
                                    existingInputField.remove();
                                    
                                    // Re-add the corresponding skeleton
                                    let skeleton = document.createElement('div');
                                    skeleton.id = `skeleton-${index}`;
                                    skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                                    skeleton.innerHTML = `
                                        <span class="label-text mb-2">
                                            <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                            <p class="italic">
                                                <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                            </p>
                                        </span>
                                        <div class="h-10 bg-gray-300 rounded w-full"></div>
                                    `;
                                    
                                    personnelNumbers.appendChild(skeleton);
                                }
                        }

                            let newInputs = personnelNumberContainerMain.querySelectorAll('input');
                            let isEmpty = checkEmptyInput(newInputs); // check if input field is empty

                            needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button

                            // add event listener to input fields to check if they are empty
                            newInputs.forEach(function(input){
                                input.addEventListener('input', function(){
                                    // check all input fields to see if they are empty
                                    let isEmpty = checkEmptyInput(newInputs);
                                    needsAssessmentBtn.disabled = isEmpty;
                                })
                                console.log(input.value)
                                console.log(isEmpty)
                            })
                            console.log(newInputs)
                        });

                        
                    })
                } 
            }

            // submit needs assessment form
            needsAssessmentBtn.addEventListener('click', function(){
                needsAssessmentBtn.innerHTML = `<span id="loading" class="loading loading-spinner loading-md text-gray-600"></span>`
                needsAssessmentBtn.disabled = true;
                let sectorSelectionValue = sectorSelection.value;
                let healthTypeValue = sectorType.value;
                let projectedPopulationValue = projectedPopulationSelect.value;
                let facilityNumbers = {};
                let personnelNumbers = {};
                let facilityNumberInputs = facilityNumbersContainerMain.querySelectorAll('input');
                let personnelNumberInputs = personnelNumberContainerMain.querySelectorAll('input');
               

                if (facilityNumberInputs.length > 0){
                    facilityNumberInputs.forEach(input => {
                        let facilityType = input.name.split('-')[1];
                        facilityNumbers[facilityType] = input.value;
                    });
                }

                if (personnelNumberInputs.length > 0){
                    personnelNumberInputs.forEach(input => {
                        let personnelType = input.name.split('-')[1];
                        personnelNumbers[personnelType] = input.value;
                    });
                }
                let data = ''

                // check if health type is facility or personnel
                if (healthTypeValue === 'facility'){
                    // send post request to server
                    data = {
                        sector: sectorSelectionValue,
                        type: healthTypeValue,
                        projectedPopulation: projectedPopulationValue,
                        facilityNumbers: facilityNumbers
                    }
                }
                else{
                    data = {
                        sector: sectorSelectionValue,
                        type: healthTypeValue,
                        projectedPopulation: projectedPopulationValue,
                        personnelNumbers: personnelNumbers
                    }
                }
                console.log(data)

                fetch('/needs-assessment/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    if (data){
                        // redirect to the needs assessment page
                        history.pushState({}, null, `/needs-assessment/${data.slug}`); 
                        document.getElementById('main').innerHTML = data.template;
                        
                        // sweet alert
                        swal({
                            title: 'Success',
                            text: 'Needs assessment submitted successfully',
                            icon: 'success',
                            button: 'Ok'
                        })
                    }
                })
                .catch(error => {
                    console.log(error)
                    needsAssessmentBtn.disabled = false;
                    needsAssessmentBtn.innerHTML = 'Assess Needs'
                    swal({
                        title: 'Error',
                        text: 'An error occured',
                        icon: 'error',
                        button: 'Ok'
                    })
                })
            })

                
            
        }
        // put functionality
        else{
            console.log('PUT')
            needsAssessmentBtn.innerText = 'Update'
            let sectorSelectionValue = sectorSelection.value;
            if (sectorSelectionValue === 'health'){
                healthTypeContainer.classList.remove('hidden');
                healthContainer.classList.remove('hidden')
            
            } else {
                healthTypeContainer.classList.add('hidden');
                healthContainer.classList.add('hidden')
                
            }
            // check the value of the health type dropdown
            let type = needType.value;
            if (type === 'facility'){
                healthFacility.classList.remove('hidden');
                healthPersonnel.classList.add('hidden');
               
            } else {
                healthFacility.classList.add('hidden');
                healthPersonnel.classList.remove('hidden');
            }

            // add event listener to sector selection dropdown
            sectorSelection.addEventListener('change', function(){
                let sectorSelectionValue = sectorSelection.value;
                if (sectorSelectionValue === 'health'){
                    healthTypeContainer.classList.remove('hidden');
                    healthContainer.classList.remove('hidden')
                    handleCheckboxChange()
                } else {
                    healthTypeContainer.classList.add('hidden');
                    healthContainer.classList.add('hidden')
                    handleCheckboxChange()
                }
            })

            // add event listener to health type dropdown
            sectorType.addEventListener('change', function(){
                let healthTypeValue = sectorType.value;
                if (healthTypeValue === 'facility'){
                    healthFacility.classList.remove('hidden');
                    healthPersonnel.classList.add('hidden');
                    handleCheckboxChange()
                    
                } else {
                    healthFacility.classList.add('hidden');
                    healthPersonnel.classList.remove('hidden');
                    handleCheckboxChange()
                }
            })

            handleCheckboxChange()

            // get original data
            let originalData = {
                sector: needsAssessmentSector.value,
                type: needType.value,
                projectedPopulation: projectedPopulationSelect.value,
                facilityNumbers: {},
                personnelNumbers: {}
            }

            let inputs = personnelNumberContainerMain.querySelectorAll('input');
            inputs.forEach(input => {
                let personnelType = input.name.split('-')[1];
                originalData.personnelNumbers[personnelType] = input.value;
            })

            let facilityInputs = facilityNumbersContainerMain.querySelectorAll('input');
            facilityInputs.forEach(input => {
                let facilityType = input.name.split('-')[1];
                originalData.facilityNumbers[facilityType] = input.value;
            })

            if (type === 'facility'){
                // remove personnelNumber from original data
                delete originalData.personnelNumbers;
            }
            else{
                // remove facilityNumbers from original data
                delete originalData.facilityNumbers;
            }

            console.log(originalData)

            needsAssessmentBtn.addEventListener('click', function(){
                needsAssessmentBtn.innerHTML = `<span id="loading" class="loading loading-spinner loading-md text-gray-600"></span>`
                needsAssessmentBtn.disabled = true;
                let sectorSelectionValue = sectorSelection.value;
                let healthTypeValue = sectorType.value;
                let projectedPopulationValue = projectedPopulationSelect.value;
                let facilityNumbers = {};
                let personnelNumbers = {};
                let facilityNumberInputs = facilityNumbersContainerMain.querySelectorAll('input');
                let personnelNumberInputs = personnelNumberContainerMain.querySelectorAll('input');

                if (facilityNumberInputs.length > 0){
                    facilityNumberInputs.forEach(input => {
                        let facilityType = input.name.split('-')[1];
                        facilityNumbers[facilityType] = input.value;
                    });
                }

                if (personnelNumberInputs.length > 0){
                    personnelNumberInputs.forEach(input => {
                        let personnelType = input.name.split('-')[1];
                        personnelNumbers[personnelType] = input.value;
                    });
                }
                let data = ''

                // check if health type is facility or personnel
                if (healthTypeValue === 'facility'){
                    // send post request to server
                    data = {
                        sector: sectorSelectionValue,
                        type: healthTypeValue,
                        projectedPopulation: projectedPopulationValue,
                        facilityNumbers: facilityNumbers
                    }
                }
                else{   
                    data = {
                        sector: sectorSelectionValue,
                        type: healthTypeValue,
                        projectedPopulation: projectedPopulationValue,
                        personnelNumbers: personnelNumbers
                    }
                }
                
                let newData = {
                    sector: sectorSelectionValue,
                    type: healthTypeValue,
                    projectedPopulation: projectedPopulationValue,
                    facilityNumbers: facilityNumbers,
                    personnelNumbers: personnelNumbers
                }

                // remove facilityNumbers from original data if type is personnel
                if (healthTypeValue === 'personnel'){
                    delete newData.facilityNumbers;
                }
                else{
                    delete newData.personnelNumbers;
                }

                // check if data is different from original data
                let isDifferent = JSON.stringify(originalData) === JSON.stringify(newData);
                console.log(isDifferent)

            

                if (!isDifferent){
                    console.log(data)
                    fetch(`/needs-assessment/${needsAssessmentSlug.value}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            
                        },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        if (data){
                            // redirect to the needs assessment page
                            history.pushState({}, null, `/needs-assessment/${data.slug}`);
                            document.getElementById('main').innerHTML = data.template;

                            // sweet alert
                            swal({
                                title: 'Success',
                                text: 'Needs assessment updated successfully',
                                icon: 'success',
                                button: 'Ok'
                            })
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        needsAssessmentBtn.disabled = false;
                        needsAssessmentBtn.innerHTML = 'Update'
                        swal({
                            title: 'Error',
                            text: 'An error occured',
                            icon: 'error',
                            button: 'Ok'
                        })
                    })
                }
                else{
                    needsAssessmentBtn.disabled = false;
                    needsAssessmentBtn.innerHTML = 'Update'
                    swal({
                        title: 'Info',
                        text: 'No changes made, make changes to data to update needs assessment',
                        icon: 'info',
                        button: 'Ok'
                    })

                }
            })





            // add event listener to projected population select

            // handle checkbox change if type is facility or personnel
            function handleCheckboxChange(){
               let originalInputData = {
                    sector: needsAssessmentSector.value,
                    type: needType.value,
                    projectedPopulation: projectedPopulationSelect.value,
                    facilityNumbers: {},
                    personnelNumbers: {}
                }

                let inputs = personnelNumberContainerMain.querySelectorAll('input');
                inputs.forEach(input => {
                    let personnelType = input.name.split('-')[1];
                    originalInputData.personnelNumbers[personnelType] = input.value;
                })

                let facilityInputs = facilityNumbersContainerMain.querySelectorAll('input');
                facilityInputs.forEach(input => {
                    let facilityType = input.name.split('-')[1];
                    originalInputData.facilityNumbers[facilityType] = input.value;
                })

                console.log(originalInputData)
                if (sectorType.value === 'facility') {
                    // if facilityNumberContainer is not empty, disable the needs assessment button
                    let inputs = facilityNumbersContainerMain.querySelectorAll('input');
                    let isEmpty = checkEmptyInput(inputs);
                    needsAssessmentBtn.disabled = isEmpty;
                    console.log(isEmpty)

                    inputs.forEach(input => {
                        input.addEventListener('input', function(){
                            // check all input fields to see if they are empty
                            let isEmpty = checkEmptyInput(inputs);
                            needsAssessmentBtn.disabled = isEmpty;
                        })
                    })

                    // if inputs is less than 4, append corresponding skeletons to the facilityNumbersContainer
                    if (inputs.length < 4){
                        for (let i = inputs.length; i < 4; i++) {
                            let skeleton = document.createElement('div');
                            skeleton.id = `skeleton-${i}`;
                            skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                            skeleton.innerHTML = `
                                <span class="label-text mb-2">
                                    <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                    <p class="italic">
                                        <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                    </p>
                                </span>
                                <div class="h-10 bg-gray-300 rounded w-full"></div>
                            `;
                            facilityNumbersContainer.appendChild(skeleton);
                        }
                    }

                    // add event listener to facility checkboxes
                    facilityCheckboxes.forEach((checkbox, index) => {
                        checkbox.addEventListener('change', function(e) {
                            // find it corresponding div and input
                            let div = document.getElementById(`facilityNumber-${e.target.value}`)
                            console.log(div)

                            if (!div){
                                let facilityType = e.target.value;
                                const inputFieldId = `facilityNumber-${facilityType}`;
                                facilityType = facilityType.charAt(0).toUpperCase() + facilityType.slice(1);
                                
                                const inputField = document.getElementById(inputFieldId) || document.createElement('div');
                                inputField.id = inputFieldId;
                                
                                inputField.innerHTML = `
                                    <div class="form-control" id="facilityNumber-${e.target.value}">
                                        <span class="label-text mb-2">${facilityType}
                                            <p class="italic" style="font-style:italic">(enter number of ${facilityType}s)</p>

                                        <input id=${facilityType.replace(' ,', '')} value="" type="number" min="1" name=facilityNumber-${facilityType}" class="input mt-2 input-bordered w-full" />
                                    </div>
                                `;
                                let facilityInput = inputField.querySelector(`input[id=${facilityType.replace(' ', '')}]`)

                                if (inputs){
                                    inputs.forEach(input => {
                                        
                                        if (input.id === facilityType){
                                            facilityInput.value = input.value
                                        }
                                        console.log(input.id, facilityType)
                                    })
                                }
                                // remove the corresponding skeleton
                                let skeleton = document.getElementById(`skeleton-${index}`);
                                if (skeleton){
                                    skeleton.remove();
                                }

                                facilityNumbersContainer.appendChild(inputField);
                            
                            }
                                
                            
                            else{
                                console.log(e, 'unchecked')
                                let div = document.getElementById(`facilityNumber-${e.target.value}`)
                                
                                div.remove()

                                // add the corresponding skeleton
                                let skeleton = document.createElement('div');
                                skeleton.id = `skeleton-${index}`;
                                skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                                skeleton.innerHTML = `
                                    <span class="label-text mb-2">
                                        <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                        <p class="italic">
                                            <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                        </p>
                                    </span>
                                    <div class="h-10 bg-gray-300 rounded w-full"></div>
                                `;
                                facilityNumbersContainer.appendChild(skeleton);

                            }

                            let newInputs = facilityNumbersContainer.querySelectorAll('input');
                            let isEmpty = checkEmptyInput(newInputs); // check if input field is empty
    
                            needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button
    
                            // add event listener to input fields to check if they are empty
                            newInputs.forEach(function(input){
                                input.addEventListener('input', function(){
                                    // check all input fields to see if they are empty
                                    let isEmpty = checkEmptyInput(newInputs);
                                    needsAssessmentBtn.disabled = isEmpty;
                                })
                                console.log(input.value)
                                console.log(isEmpty)
                            })
                            console.log(newInputs)

                        })
                    })
                    
                }
                    
                else {   
                    // 
                    let inputs = personnelNumberContainerMain.querySelectorAll('input');
                    let isEmpty = checkEmptyInput(inputs);
                    needsAssessmentBtn.disabled = isEmpty;
                    console.log(isEmpty)

                    inputs.forEach(input => {
                        input.addEventListener('input', function(){
                            // check all input fields to see if they are empty
                            let isEmpty = checkEmptyInput(inputs);
                            needsAssessmentBtn.disabled = isEmpty;
                        })
                    })

                     // if inputs is less than 4, append corresponding skeletons to the facilityNumbersContainer
                    if (inputs.length < 4){
                        for (let i = inputs.length; i < 4; i++) {
                            let skeleton = document.createElement('div');
                            skeleton.id = `personnel-skeleton-${i}`;
                            skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                            skeleton.innerHTML = `
                                <span class="label-text mb-2">
                                    <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                    <p class="italic">
                                        <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                    </p>
                                </span>
                                <div class="h-10 bg-gray-300 rounded w-full"></div>
                            `;
                            
                            personnelNumbers.appendChild(skeleton);
                        }
                    }

                    // add event listener to personnel checkboxes
                    personnelCheckboxes.forEach((checkbox, index) => {
                        checkbox.addEventListener('change', function(e) {
                            if (e.target.checked){
                                
                                // find it corresponding div and input
                                let div = document.getElementById(`personnelNumber-${e.target.value}`)
                                console.log(div)

                                if (!div){
                                    let personnelType = e.target.value;
                                    const inputFieldId = `personnelNumber-${personnelType}`;
                                    personnelType = personnelType.charAt(0).toUpperCase() + personnelType.slice(1);
                                    
                                    const inputField = document.getElementById(inputFieldId) || document.createElement('div');
                                    inputField.id = inputFieldId;
                                    
                                    inputField.innerHTML = `
                                        <div class="form-control" id="personnelNumber-${e.target.value}">
                                            <span class="label-text mb-2">${personnelType}
                                                <p class="italic" style="font-style:italic">(enter number of ${personnelType}s)</p>

                                            <input id=${personnelType} value="" type="number" min="1" name="personnelNumber-${personnelType}" class="input mt-2 input-bordered w-full" />
                                        </div>
                                    `;
                                    let personnelInput = inputField.querySelector(`input[id=${personnelType}]`)

                                    if (inputs){
                                        inputs.forEach(input => {
                                            
                                            if (input.id === personnelType){
                                                personnelInput.value = input.value
                                            }
                                            console.log(input.id, personnelType)
                                        })
                                    }
                                    // remove the corresponding skeleton
                                    let skeleton = document.getElementById(`personnel-skeleton-${index}`);
                                    if (skeleton){
                                        skeleton.remove();
                                    }
                                    console.log('INDEX',index)
                                    personnelNumbers.appendChild(inputField);
                                
                                }
                                
                            }
                            else{
                                console.log(e, 'unchecked')
                                let div = document.getElementById(`personnelNumber-${e.target.value}`)
                                
                                div.remove()
                                // add the corresponding skeleton
                                let skeleton = document.createElement('div');
                                skeleton.id = `personnel-skeleton-${index}`;
                                skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                                skeleton.innerHTML = `
                                    <span class="label-text mb-2">
                                        <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                        <p class="italic">
                                            <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                        </p>
                                    </span>
                                    <div class="h-10 bg-gray-300 rounded w-full"></div>
                                `;
                                personnelNumbers.appendChild(skeleton);

                            }

                            let newInputs = personnelNumberContainerMain.querySelectorAll('input');
                            let isEmpty = checkEmptyInput(newInputs); // check if input field is empty
    
                            needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button
    
                            // add event listener to input fields to check if they are empty
                            newInputs.forEach(function(input){
                                input.addEventListener('input', function(){
                                    // check all input fields to see if they are empty
                                    let isEmpty = checkEmptyInput(newInputs);
                                    needsAssessmentBtn.disabled = isEmpty;
                                })
                                console.log(input.value)
                                console.log(isEmpty)
                            })
                            console.log(newInputs)

                            
                        })
                    })
                }
                                    
            }

            // handle put request

            
        }

    // check if input field is empty
    function checkEmptyInput(inputs){
        let empty = false;
        if (inputs.length === 0){
            empty = true;
        }
        else{
            inputs.forEach(function(input){
                if (input.value === ''){
                    empty = true;
                }
            })
        }
        return empty;
        
    }


        
    
       
    
}       