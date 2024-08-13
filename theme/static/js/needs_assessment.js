
// function to handle needs assessment page
export const main = () => {
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
        let school = document.getElementById('classroom')
        let dualDesk = document.getElementById('dual-desk')
        let educationSectorType = document.getElementById('educationSectorType')

        let schoolContainer = document.getElementById('education')
        let waterContainer = document.getElementById('water')
        let utilityTypeContainer = document.getElementById('utilityTypeContainer')
        let utilitySectorType = document.getElementById('utilitySectorType')
        let waterSourceCheckbox = document.querySelectorAll('.water-source-checkbox')
        let waterQuantities = document.getElementById('waterQuantities')
        let schoolTypeContainer = document.getElementById('educationTypeContainer')
        let schoolCheckboxes = document.querySelectorAll('.education-checkbox')
        let utility = document.getElementById('utility')
        let sanitation = document.getElementById('sanitation')
        let sanitationTypeContainer = document.getElementById('sanitationTypeContainer')
        let sanitationType = document.getElementById('sanitationType')
        let toilet = document.getElementById('toilet')
        let toiletCheckboxs = document.querySelectorAll('.toilet-checkbox')
        let toiletNumbers = document.getElementById('toiletNumbers')
        let skipContainer = document.getElementById('skipContainer')
        let skipContainerCheckbox = document.querySelector('.skip-container-checkbox')
        let skipContainerNumbers = document.getElementById('skipContainerNumbers')
        let dualDeskCheckboxes = document.querySelectorAll('.dual-desk-checkbox')

        let dualDeskNumbers = document.getElementById('dualDeskNumbers')
        let schoolNumbers = document.getElementById('schoolNumbers')

        let populationProjection = document.getElementById('population-projection')

        let educationEnrolment = document.getElementById('education-enrolment')

        let allCheckboxes = document.querySelectorAll('.checkbox')
        console.log(allCheckboxes)

    

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
                schoolContainer.classList.add('hidden')
                schoolTypeContainer.classList.add('hidden');
                educationEnrolment.classList.add('hidden')
                utility.classList.add('hidden')
                utilityTypeContainer.classList.add('hidden')
                utilitySectorType.classList.add('hidden')
                populationProjection.classList.remove('hidden')
                sanitation.classList.add('hidden')
                needsAssessmentBtn.innerText = 'Assess Needs'

                // uncheck all checkboxes
                allCheckboxes.forEach(checkbox => {
                    if (checkbox.checked){
                        checkbox.click()
                    }
                })
                
            } 
            else if (sectorSelectionValue === 'education'){
                needsAssessmentBtn.innerText = 'Project and Assess Needs'
                schoolContainer.classList.remove('hidden')
                schoolTypeContainer.classList.remove('hidden');
                educationEnrolment.classList.remove('hidden')
                populationProjection.classList.add('hidden')
                healthContainer.classList.add('hidden')
                healthTypeContainer.classList.add('hidden');
                utilityTypeContainer.classList.add('hidden')
                waterContainer.classList.add('hidden')

                // uncheck all health checkboxes
                facilityCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                })
                personnelCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                })
            
            }
            else if (sectorSelectionValue === 'water'){
                waterContainer.classList.remove('hidden')
                utilityTypeContainer.classList.remove('hidden')
                healthContainer.classList.add('hidden')
                healthTypeContainer.classList.add('hidden');
                schoolContainer.classList.add('hidden')
                schoolTypeContainer.classList.add('hidden');
                educationEnrolment.classList.add('hidden')
                populationProjection.classList.add('hidden')


            }
            // check the value of the health type dropdown
            let type = sectorType.value;
            if (type === 'facility'){
                healthFacility.classList.remove('hidden');
                healthPersonnel.classList.add('hidden');

                // uncheck personnel checkboxes
                personnelCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                })
               
            } else if (type === 'personnel'){
                healthFacility.classList.add('hidden');
                healthPersonnel.classList.remove('hidden');

                // uncheck facility checkboxes
                facilityCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                })
            }
            
            if (educationSectorType.value === 'dual_desk'){
                dualDesk.classList.remove('hidden');
                school.classList.add('hidden');

                // uncheck school checkboxes
                schoolCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                })
            }
            else if(educationSectorType.value === 'classroom'){
                dualDesk.classList.add('hidden');
                school.classList.remove('hidden');

                // uncheck dual desk checkboxes
                dualDeskCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                })
            }

            // add event listener to sector selection dropdown
            sectorSelection.addEventListener('change', function(){
                let sectorSelectionValue = sectorSelection.value;
                if (sectorSelectionValue === 'health'){
                    // show health type dropdown and health container
                    healthTypeContainer.classList.remove('hidden');
                    healthContainer.classList.remove('hidden')
                    needsAssessmentBtn.innerText = 'Assess Needs'
                    educationEnrolment.classList.add('hidden')
                    populationProjection.classList.remove('hidden')

                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })

                    // set sectorType value to facility
                    

                    // hide school container and school type dropdown
                    schoolContainer.classList.add('hidden')
                    schoolTypeContainer.classList.add('hidden');
                    utility.classList.add('hidden')
                    utilitySectorType.classList.add('hidden')
                    utilityTypeContainer.classList.add('hidden')

                    
                    handleHealthCheckboxChange() // handle checkbox change if type is facility or personnel

                    
                    
                    swal({
                        title: 'Info',
                        text: 'Please note that you are assessing needs for the health sector',
                        icon: 'info',
                        button: 'Ok'
                    })
                   
                    
                } else if (sectorSelectionValue === 'education'){
                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })

                    // show school container and school type dropdown
                    healthTypeContainer.classList.add('hidden');
                    healthContainer.classList.add('hidden')
                    educationEnrolment.classList.remove('hidden')
                    populationProjection.classList.add('hidden')

                    // hide health container and health type dropdown
                    schoolContainer.classList.remove('hidden')
                    schoolTypeContainer.classList.remove('hidden');
                    
                    utility.classList.add('hidden')
                    utilitySectorType.classList.add('hidden')
                    utilityTypeContainer.classList.add('hidden')
                    educationEnrolment.parentElement.parentElement.parentElement.parentElement.scrollIntoView({behavior: 'smooth'})

                    // check if there exits education enrolment projection
                    // if there is no education enrolment projection, show sweet alert
                    let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                    console.log(educationEnrollmentSelect)
                    if (educationEnrollmentSelect){
                        let slug = educationEnrollmentSelect.value;
                        let url = '/get-population-projection-details/' + slug;
                        htmx.ajax('GET', url, {
                            target: '#educationEnrolmentInfo',
                            swap: 'innerHTML'
                        })
                        
                    }
                    else{
                        needsAssessmentBtn.innerText = 'Project and Assess Needs'
                        swal({
                            title: 'Info',
                            text: 'No education enrolment projection found. Please project education enrolment and assess needs',
                            icon: 'info',
                            button: 'Ok'
                        })
                    }
                    

                    handleEducationCheckboxChange() // handle checkbox change if type is dual desk or classroom

                    // set time out to show sweet alert for letting user know that education enrolment projection will be done before needs assessment
                    
                    swal({
                        title: 'Info',
                        text: 'Please note that you will be required to do an education enrolment projection before you can assess the needs of the education sector',
                        icon: 'info',
                        button: 'Ok'
                    })
                    

                }
                else if (sectorSelectionValue === 'utility'){
                    utility.classList.remove('hidden')
                    utilityTypeContainer.classList.remove('hidden')
                    utilitySectorType.classList.remove('hidden')
                    healthContainer.classList.add('hidden')
                    healthTypeContainer.classList.add('hidden');
                    schoolContainer.classList.add('hidden')
                    schoolTypeContainer.classList.add('hidden');
                    educationEnrolment.classList.add('hidden')
                    populationProjection.classList.remove('hidden')

                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })


                    swal({
                        title: 'Info',
                        text: 'Please note that you are assessing needs for the utility sector',
                        icon: 'info',
                        button: 'Ok'
                    })

                    handleWaterSourceCheckboxChange() // handle checkbox change if type is water source
                }
            })

            // add event listener to health type dropdown
            sectorType.addEventListener('change', function(){
                let healthTypeValue = sectorType.value;
                if (healthTypeValue === 'facility'){
                    healthFacility.classList.remove('hidden');
                    healthPersonnel.classList.add('hidden');
                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })
                    handleHealthCheckboxChange()
                    
                    
                } else if (healthTypeValue === 'personnel'){
                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })
                    
                    healthFacility.classList.add('hidden');
                    healthPersonnel.classList.remove('hidden');
                    handleHealthCheckboxChange()
                    
                }
               
            })

            // add event listener to education sector type dropdown
            educationSectorType.addEventListener('change', function(){
                let educationSectorTypeValue = educationSectorType.value;
                if (educationSectorTypeValue === 'dual_desk'){
                    dualDesk.classList.remove('hidden');
                    school.classList.add('hidden');

                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })
                    handleEducationCheckboxChange()

                }
                else if (educationSectorTypeValue === 'classroom'){
                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })
                    dualDesk.classList.add('hidden');
                    school.classList.remove('hidden');
                    handleEducationCheckboxChange()
                }
            })

            // add event listener to utilitySectorType dropdown
            utilitySectorType.addEventListener('change', function(){
                let utilitySectorTypeValue = utilitySectorType.value;
                if (utilitySectorTypeValue === 'water'){
                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })
                    waterContainer.classList.remove('hidden')
                    sanitation.classList.add('hidden')
                    sanitationTypeContainer.classList.add('hidden')
                    handleWaterSourceCheckboxChange()
                }
                else if (utilitySectorTypeValue === 'sanitation'){
                    // uncheck all checkboxes
                    allCheckboxes.forEach(checkbox => {
                        if (checkbox.checked){
                            checkbox.click()
                        }
                    })
                    waterContainer.classList.add('hidden')
                    sanitationTypeContainer.classList.remove('hidden')
                    sanitation.classList.remove('hidden')
                    console.log(sanitationType.value)
                    if (sanitationType.value === 'toilet'){
                        toilet.classList.remove('hidden')
                        skipContainer.classList.add('hidden')
                        handleToiletCheckboxChange()
                    }
                    else{
                        toilet.classList.add('hidden')
                        skipContainer.classList.remove('hidden')
                        handleSkipContainerCheckboxChange()
                    }
                }
                
                
            })

            // add event listener to sanitationTypeContainer dropdown
            sanitationType.addEventListener('change', function(){
                let sanitationTypeValue = sanitationType.value;
                if (sanitationTypeValue === 'toilet'){
                    toilet.classList.remove('hidden')
                    skipContainer.classList.add('hidden')
                    handleToiletCheckboxChange()
                }
                else{
                    toilet.classList.add('hidden')
                    skipContainer.classList.remove('hidden')
                    handleSkipContainerCheckboxChange()
                }
            })


            handleHealthCheckboxChange()
           

            // add event listener to projected population select

            // handle checkbox change if type is facility or personnel
            function handleHealthCheckboxChange(){
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

                                facilityNumbersContainer.prepend(inputField);
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

            
            // handle checkbox change if type is dual desk or classroom
            function handleEducationCheckboxChange(){
                if (educationSectorType.value){
                    if (educationSectorType.value === 'dual_desk') {
                        // if facilityNumberContainer is not empty, disable the needs assessment button
                        let inputs = dualDeskNumbers.querySelectorAll('input');
                        let educationEnrolmentInputs = educationEnrolment.querySelectorAll('input');
                        console.log(inputs)
                        let isEmpty = checkEmptyInput(inputs);
                        
                        
                        let educationIsEmpty = checkEmptyInput(educationEnrolmentInputs);

                        let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                        if(educationEnrollmentSelect.value){
                            var educationEnrollmentSelectIsEmpty = false;
                        }

                        if (isEmpty || educationIsEmpty || educationEnrollmentSelectIsEmpty){
                            needsAssessmentBtn.disabled = true;
                        }
                        else{
                            needsAssessmentBtn.disabled = false
                        }
                        
                        
                        // add event listener to facility checkboxes
                        dualDeskCheckboxes.forEach((checkbox, index) =>{
                            checkbox.addEventListener('change', function(e){
                                console.log(e.target)
                                let dualDeskType = e.target.value;
                                const inputFieldId = `${dualDeskType}`;
                                dualDeskType = dualDeskType.charAt(0).toUpperCase() + dualDeskType.slice(1);
                    
                                let inputField = document.createElement('div');
                                inputField.id = inputFieldId;
                                let info = `enter total no. of ${dualDeskType}'s dual desks`
                                if (e.target.checked) {
                                    inputField.innerHTML = `
                                        <div class="form-control">
                                            <span class="label-text mb-2">${dualDeskType}-dual desk 
                                                <p class="italic" style="font-style:italic">(${truncateword(info, 5)})</p>

                                            <input id=${dualDeskType.replace(' ', '')} value="" type="number" min="1" name="dualDeskNumber-${dualDeskType}" class="input mt-2 input-bordered w-full" />
                                        </div>
                                    `;
                                    // Remove the corresponding skeleton
                                    const skeleton = document.querySelector(`#dualDeskSkeleton-${index}`);

                                    if (skeleton) {
                                        skeleton.remove();
                                    }

                                    dualDeskNumbers.prepend(inputField);
                                }
                                else {
                                    const existingInputField = dualDeskNumbers.querySelector(`#${inputFieldId}`);
                                    console.log(existingInputField)
                                    if (existingInputField) {
                                        existingInputField.remove();
                                        
                                        // Re-add the corresponding skeleton
                                        let skeleton = document.createElement('div');
                                        skeleton.id = `dualDeskSkeleton-${index}`;
                                        skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                                        skeleton.innerHTML = `
                                            <span class="label-text
                                            mb-2">
                                                <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                                <p class="italic">
                                                    <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                                </p>
                                            </span>
                                            <div class="h-10 bg-gray-300 rounded w-full"></div>
                                        `;

                                        dualDeskNumbers.appendChild(skeleton);
                                    }
                                }
                                let newInputs = dualDeskNumbers.querySelectorAll('input');
                                let isEmpty = checkEmptyInput(newInputs); // check if input field is empty


                                let educationEnrolmentInputs = educationEnrolment.querySelectorAll('input');

                                let educationIsEmpty = checkEmptyInput(educationEnrolmentInputs);

                                let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                        
                                
                                if(!educationEnrollmentSelect){
                                    if(isEmpty || educationIsEmpty ){
                                        needsAssessmentBtn.disabled = true;
                                    }
                                    else{
                                        needsAssessmentBtn.disabled = false;
                                    }
                                }
                                else{
                                    if(isEmpty){
                                        needsAssessmentBtn.disabled = true;
                                    }
                                    else{
                                        needsAssessmentBtn.disabled = false;
                                    }
                                }
                                            

                                // add event listener to input fields to check if they are empty
                                console.log(newInputs)
                                newInputs.forEach(input =>{
                                    input.addEventListener('input', function(){
                                        // check all input fields to see if they are empty
                                        let isEmpty = checkEmptyInput(newInputs);

                                        let isEducationEmpty = checkEmptyInput(educationEnrolmentInputs);

                                        let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                                        
                                        if(!educationEnrollmentSelect){
                                            
                                            if(isEmpty || isEducationEmpty ){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                        else{
                                            if(isEmpty){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                            

                                        console.log(isEmpty, isEducationEmpty)
                                    })
                                })

                                educationEnrolmentInputs.forEach(input =>{
                                    input.addEventListener('input', function(){
                                        // check all input fields to see if they are empty
                                        let educationIsEmpty = checkEmptyInput(educationEnrolmentInputs);
                                        
                                        let isEmpty = checkEmptyInput(newInputs);

                                        let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                                        
                                        if(!educationEnrollmentSelect){
                                            
                                            if(isEmpty || educationIsEmpty ){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                        else{
                                            if(isEmpty){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                        console.log(educationIsEmpty, isEmpty)

                                        
                                    })
                                })
                            })


                        })
                    }
                    else{
                        let inputs = schoolNumbers.querySelectorAll('input');
                        let isEmpty = checkEmptyInput(inputs);
                        

                        let educationEnrolmentInputs = educationEnrolment.querySelectorAll('input');

                        let educationIsEmpty = checkEmptyInput(educationEnrolmentInputs);

                        if (isEmpty || educationIsEmpty){
                            needsAssessmentBtn.disabled = true;
                        }
                        else{
                            needsAssessmentBtn.disabled = false
                        }
                        
                        schoolCheckboxes.forEach((schCheckbox, index) =>{
                            schCheckbox.addEventListener('change', function(e){
                                console.log(e.target)
                                let schoolType = e.target.value;
                                const inputFieldId = `${schoolType}`;
                                schoolType = schoolType.charAt(0).toUpperCase() + schoolType.slice(1);
                                
                                
                                let inputField = document.createElement('div');
                                inputField.id = inputFieldId;
                                let info = `enter total no. of ${schoolType} classrooms`
                                if (e.target.checked) {
                                    
                                    inputField.innerHTML = `
                                        <div class="form-control">
                                            <span class="label-text mb-2">${schoolType} - classroom
                                                <p class="italic" style="font-style:italic">(${truncateword(info, 5)})
                                                </p>

                                            <input id=${schoolType.replace(' ', '')} value="" type="number" min="1" name="schoolNumber-${schoolType}" class="input mt-2 input-bordered w-full" />
                                        </div>
                                    `;
                                    // Remove the corresponding skeleton
                                    const skeleton = document.querySelector(`#schoolSkeleton-${index}`);

                                    if (skeleton) {
                                        skeleton.remove();
                                    }
                                    
                                    // prepend one input field to the schoolNumbers container
                                    schoolNumbers.prepend(inputField)
                                    
                                }
                                else {
                                    const existingInputField = document.getElementById(inputFieldId);
                                    if (existingInputField) {
                                        existingInputField.remove();
                                        
                                        // Re-add the corresponding skeleton
                                        let skeleton = document.createElement('div');
                                        skeleton.id = `schoolSkeleton-${index}`;
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

                                        schoolNumbers.appendChild(skeleton);
                                    }
                                }
                               
                                let newInputs = schoolNumbers.querySelectorAll('input');
                                let isEmpty = checkEmptyInput(newInputs); // check if input field is empty

                                let educationEnrolmentInputs = educationEnrolment.querySelectorAll('input');

                                let educationIsEmpty = checkEmptyInput(educationEnrolmentInputs);

                                let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                        
                                
                                if(!educationEnrollmentSelect){
                                    if(isEmpty || educationIsEmpty ){
                                        needsAssessmentBtn.disabled = true;
                                    }
                                    else{
                                        needsAssessmentBtn.disabled = false;
                                    }
                                }
                                else{
                                    if(isEmpty){
                                        needsAssessmentBtn.disabled = true;
                                    }
                                    else{
                                        needsAssessmentBtn.disabled = false;
                                    }
                                }

                                // add event listener to input fields to check if they are empty
                                console.log(newInputs)
                                newInputs.forEach(input =>{
                                    input.addEventListener('input', function(){
                                        // check all input fields to see if they are empty
                                        let isEmpty = checkEmptyInput(newInputs);
                                        
                                        let isEducationEmpty = checkEmptyInput(educationEnrolmentInputs);

                                        let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                        
                                
                                        if(!educationEnrollmentSelect){
                                            if(isEmpty || isEducationEmpty ){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                        else{
                                            if(isEmpty){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                    })

                                })

                                educationEnrolmentInputs.forEach(input =>{
                                    input.addEventListener('input', function(){
                                        // check all input fields to see if they are empty
                                        let educationIsEmpty = checkEmptyInput(educationEnrolmentInputs);
                                        
                                        let isEmpty = checkEmptyInput(newInputs);

                                        
                                        if(!educationEnrollmentSelect){
                                            if(isEmpty || educationIsEmpty ){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                        else{
                                            if(isEmpty){
                                                needsAssessmentBtn.disabled = true;
                                            }
                                            else{
                                                needsAssessmentBtn.disabled = false;
                                            }
                                        }
                                    })
                                })
                            })
                        })
                    }
                }
            }

            // handle checkbox change if type is water source
            function handleWaterSourceCheckboxChange(){
                waterSourceCheckbox.forEach((checkbox, index) => {
                    checkbox.addEventListener('change', function(e){
                        let waterSource = e.target.value;
                        const inputFieldId = `${waterSource}`;
                        waterSource = waterSource.charAt(0).toUpperCase() + waterSource.slice(1);

                        let inputField = document.createElement('div');
                        inputField.id = inputFieldId;

                        if (e.target.checked){
                            console.log('checked')
                            inputField.innerHTML = `
                                <div class="form-control">
                                    <span class="label-text mb-2">${waterSource}
                                        <p class="italic" style="font-style:italic">(enter number of ${waterSource}s)</p>

                                    <input id=${waterSource.replace(' ', '')} value="" type="number" min="1" name="waterSourceNumber-${waterSource}" class="input mt-2 input-bordered w-full" />
                                </div>
                            `;
                            // Remove the corresponding skeleton
                            const skeleton = document.querySelector(`#waterSkeleton-${index}`);

                            if (skeleton) {
                                skeleton.remove();
                            }
                            waterQuantities.prepend(inputField);
                        }
                        else{
                            const existingInputField = document.getElementById(inputFieldId);
                            if (existingInputField){
                                existingInputField.remove();
                                
                                // Re-add the corresponding skeleton
                                let skeleton = document.createElement('div');
                                skeleton.id = `waterSkeleton-${index}`;
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

                                waterQuantities.appendChild(skeleton);
                            }
                        }
                        let newInputs = waterQuantities.querySelectorAll('input');

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

                    })
                })
            }

            // handle checkbox change if type is toilet
            function handleToiletCheckboxChange(){
                toiletCheckboxs.forEach((checkbox, index) => {
                    checkbox.addEventListener('change', function(e){
                        let toiletType = e.target.value;
                        const inputFieldId = `${toiletType}`;
                        toiletType = toiletType.charAt(0).toUpperCase() + toiletType.slice(1);

                        let inputField = document.createElement('div');
                        inputField.id = inputFieldId;

                        if (e.target.checked){
                            console.log('checked')
                            inputField.innerHTML = `
                                <div class="form-control">
                                    <span class="label-text mb-2">${toiletType}
                                        <p class="italic" style="font-style:italic">(enter number of ${toiletType}s)</p>

                                    <input id=${toiletType.replace(' ', '')} value="" type="number" min="1" name="toiletNumber-${toiletType}" class="input mt-2 input-bordered w-full" />
                                </div>
                            `;
                            // Remove the corresponding skeleton
                            const skeleton = document.querySelector(`#toiletSkeleton-${index}`);

                            if (skeleton) {
                                skeleton.remove();
                            }
                            toiletNumbers.prepend(inputField);
                        }
                        else{
                            const existingInputField = document.getElementById(inputFieldId);
                            if (existingInputField){
                                existingInputField.remove();

                                // Re-add the corresponding skeleton
                                let skeleton = document.createElement('div');
                                skeleton.id = `toiletSkeleton-${index}`;
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
                                toiletNumbers.appendChild(skeleton);
                            }
                        }
                        let newInputs = toiletNumbers.querySelectorAll('input');

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

                    })
                })
            }

            // handle checkbox change if type is skip container
            function handleSkipContainerCheckboxChange(){
                skipContainerCheckbox.addEventListener('change', function(e){
                        let skipType = e.target.value;
                        const inputFieldId = skipType;
                        skipType = skipType.charAt(0).toUpperCase() + skipType.slice(1);

                        let inputField = document.createElement('div');
                        inputField.id = inputFieldId;

                        if (e.target.checked){
                            console.log('checked')
                            inputField.innerHTML = `
                                <div class="form-control">
                                    <span class="label-text
                                    mb-2">${skipType}
                                        <p class="italic" style="font-style:italic">(enter number of ${skipType}s)</p>

                                    <input id=${skipType.replace(' ', '')} value="" type="number" min="1" name="skipNumber-${skipType}" class="input mt-2 input-bordered w-full" />
                                </div>
                            `;
                            // Remove the corresponding skeleton
                            const skeleton = document.querySelector(`#skipSkeleton-${0}`);

                            if (skeleton) {
                                skeleton.remove();
                            }
                            skipContainerNumbers.prepend(inputField);
                        }
                        else{
                            const existingInputField = document.getElementById(inputFieldId);
                            console.log(existingInputField)
                            if (existingInputField){
                                existingInputField.remove();

                                // Re-add the corresponding skeleton
                                let skeleton = document.createElement('div');
                                skeleton.id = `skipSkeleton-${0}`;
                                skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
                                skeleton.innerHTML = `
                                    <span class="label-text
                                    mb-2">
                                        <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                                        <p class="italic">
                                            <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
                                        </p>
                                    </span>
                                    <div class="h-10 bg-gray-300 rounded w-full"></div>
                                `;
                                skipContainerNumbers.appendChild(skeleton);
                            }
                        }
                        let newInputs = skipContainerNumbers.querySelectorAll('input');

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

                })
                
            }
            

            function truncateword(str, numWords) {
                if (!str) return '';
                
                const words = str.split(' ');
                if (words.length <= numWords) {
                    return str;
                }
                
                return words.slice(0, numWords).join(' ') + '...';
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
                if (sectorSelectionValue === 'health'){
                    if (healthTypeValue === 'facility'){
                        // send post request to server
                        data = {
                            sector: sectorSelectionValue,
                            type: healthTypeValue,
                            projectedPopulation: projectedPopulationValue,
                            facilityNumbers: facilityNumbers
                        }
                    }
                    else if (healthTypeValue === 'personnel'){
                        data = {
                            sector: sectorSelectionValue,
                            type: healthTypeValue,
                            projectedPopulation: projectedPopulationValue,
                            personnelNumbers: personnelNumbers
                        }
                    }
                    console.log(data)
                    htmx.ajax('POST', '/needs-assessment/',  {
                        target: '#main',
                        swap: 'innerHTML',
                        values: data,
                    })
                    .then(() => {
                        
                        swal({
                            title: 'Success',
                            text: 'Needs assessment submitted successfully',
                            icon: 'success',
                            button: 'Ok'
                        })
                    })


                }
                else if (sectorSelectionValue === 'education'){
                    let educationEnrollmentSelect = document.getElementById('educationEnrollmentSelect');
                   let educationEnrolmentInputs = educationEnrolment.querySelectorAll('input');
                    if (educationSectorType.value === 'dual_desk'){
                        if (!educationEnrollmentSelect){
                            data = {
                                sector: sectorSelectionValue,
                                type: educationSectorType.value,
                                dualDeskNumbers: {},
                                baseYear:document.getElementById('baseYearSelect').value,
                                projectionYear:document.getElementById('projectionYearSelect').value,
                                growthRate:'',
                                basePopulation: '',
                                area: document.getElementById('area').value,
                                areaType: document.querySelectorAll('input[name="areaType"]:checked')[0].value
                            }
                            let dualDeskInputs = dualDeskNumbers.querySelectorAll('input');
                            dualDeskInputs.forEach(input => {
                                let dualDeskType = input.name.split('-')[1];
                                data.dualDeskNumbers[dualDeskType] = input.value;
                            })
                            educationEnrolmentInputs.forEach(input => {
                                if (input.id === 'growthRate'){
                                    data.growthRate = parseFloat(input.value);
                                }
                                else if (input.id === 'basePopulation'){
                                    data.basePopulation = input.value;
                                }  

                            })
                        }
                        else{
                            data = {
                                sector: sectorSelectionValue,
                                type: educationSectorType.value,
                                dualDeskNumbers: {},
                                populationProjection: educationEnrollmentSelect.value,
                            }
                            let dualDeskInputs = dualDeskNumbers.querySelectorAll('input');
                            dualDeskInputs.forEach(input => {
                                let dualDeskType = input.name.split('-')[1];
                                data.dualDeskNumbers[dualDeskType] = input.value;
                            })
                        }

                    }
                    else if (educationSectorType.value === 'classroom'){
                        if (!educationEnrollmentSelect){
                            data = {
                                sector: sectorSelectionValue,
                                type: educationSectorType.value,
                                schoolNumbers: {},
                                baseYear:document.getElementById('baseYearSelect').value,
                                projectionYear:document.getElementById('projectionYearSelect').value,
                                growthRate:'',
                                basePopulation: '',
                                area: document.getElementById('area').value,
                                areaType: document.querySelectorAll('input[name="areaType"]:checked')[0].value

                            }
                            let schoolInputs = schoolNumbers.querySelectorAll('input');
                            schoolInputs.forEach(input => {
                                // check if input field name contains a - for example Pre-School
                                let schoolType = input.name.split('-')[1];
                                if (schoolType === 'Pre'){
                                    schoolType = 'Pre-School'
                                }
                                data.schoolNumbers[schoolType] = input.value;
                            })
                            educationEnrolmentInputs.forEach(input => {
                                if (input.id === 'growthRate'){
                                    data.growthRate = input.value;
                                }
                                else if (input.id === 'basePopulation'){
                                    data.basePopulation = input.value;
                                }  

                            })
                        }
                        else{
                            data = {
                                sector: sectorSelectionValue,
                                type: educationSectorType.value,
                                schoolNumbers: {},
                                populationProjection: educationEnrollmentSelect.value
                            }
                            let schoolInputs = schoolNumbers.querySelectorAll('input');
                            schoolInputs.forEach(input => {
                                // check if input field name contains a - for example Pre-School
                                let schoolType = input.name.split('-')[1];
                                if (schoolType === 'Pre'){
                                    schoolType = 'Pre-School'
                                }
                                data.schoolNumbers[schoolType] = input.value;
                            })
                            educationEnrolmentInputs.forEach(input => {
                                if (input.id === 'growthRate'){
                                    data.growthRate = input.value;
                                }
                                else if (input.id === 'basePopulation'){
                                    data.basePopulation = input.value;
                                }  

                            })
                        }
                    }

                    
                    if (!educationEnrollmentSelect){
                        if (data.growthRate > 0 && data.basePopulation > 0){
                            console.log(JSON.stringify(data))
                            htmx.ajax('POST', '/education-needs-assessment/',{
                                target: '#main',
                                swap: 'innerHTML',
                                pushUrl: true,
                                values:data,  
                            })
                            .then(response =>{
                                
                                swal({
                                    title: 'Success',
                                    text: 'Needs assessment submitted successfully',
                                    icon: 'success',
                                    button: 'Ok'
                                })

                                
                            })
                            

                        }
                        else{
                            swal({
                                title: 'Error',
                                text: 'Please growth rate and base population must be greater than 0',
                                icon: 'error',
                                button: 'Ok'
                            })
                        }
                    }
                    else{
                        console.log(JSON.stringify(data))
                            htmx.ajax('POST', '/education-needs-assessment/',{
                                target: '#main',
                                swap: 'innerHTML',
                                pushUrl: true,
                                values:data,  
                            })
                            .then(response =>{
                                
                                swal({
                                    title: 'Success',
                                    text: 'Needs assessment submitted successfully',
                                    icon: 'success',
                                    button: 'Ok'
                                })

                                
                            })
                    }


                }
                else if (sectorSelectionValue === 'utility'){
                    if (utilitySectorType.value === 'water'){
                        let waterSourceInputs = waterQuantities.querySelectorAll('input');
                        let waterSourceNumbers = {};
                        waterSourceInputs.forEach(input => {
                            let waterSource = input.name.split('-')[1];
                            waterSourceNumbers[waterSource] = input.value;
                        })
                        data = {
                            sector: sectorSelectionValue,
                            type: utilitySectorType.value,
                            waterSourceNumbers: waterSourceNumbers,
                            populationProjection: projectedPopulationValue
                        }
                        console.log(data)
                        htmx.ajax('POST', '/utility-needs-assessment/',{
                            target: '#main',
                            swap: 'innerHTML',
                            pushUrl: true,
                            values:data,
                        })
                        .then(response =>{
                            swal({
                                title: 'Success',
                                text: 'Needs assessment submitted successfully',
                                icon: 'success',
                                button: 'Ok'
                            })
                        })
                    }
                    else if (utilitySectorType.value == 'sanitation'){
                        if (sanitationType.value == 'toilet'){
                            let toiletInputs = toiletNumbers.querySelectorAll('input')
                            let toiletSourceNumbers = {}
                            toiletInputs.forEach(input => {
                               let toiletSource = input.name.split('-')[1]
                               toiletSourceNumbers[toiletSource] = input.value 
                            })
                            data = {
                                sector: sectorSelectionValue,
                                type:sanitationType.value,
                                toiletNumbers: toiletSourceNumbers,
                                populationProjection: projectedPopulationValue
                            }
                            htmx.ajax('POST', '/utility-needs-assessment/',{
                                target: '#main',
                                swap: 'innerHTML',
                                pushUrl: true,
                                values:data,
                            })
                            .then(response =>{
                                swal({
                                    title: 'Success',
                                    text: 'Needs assessment submitted successfully',
                                    icon: 'success',
                                    button: 'Ok'
                                })
                            })
                            
                        }
                        else if (sanitationType.value == 'wasteDisposal'){
                            let skipContainerInputs = skipContainerNumbers.querySelectorAll('input');
                            console.log(skipContainerInputs)
                            let skipNumbers = {}
                            skipContainerInputs.forEach(input => {
                                let skipContainer = input.name.split('-')[1];
                                skipNumbers[skipContainer] = input.value;
                            })
                            data = {
                                sector: sectorSelectionValue,
                                type: sanitationType.value,
                                skipContainerNumbers: skipNumbers,
                                populationProjection: projectedPopulationValue
                            }
                            console.log(data)
                            htmx.ajax('POST', '/utility-needs-assessment/',{
                                target: '#main',
                                swap: 'innerHTML',
                                pushUrl: true,
                                values:data,
                            })
                            .then(response =>{
                                swal({
                                    title: 'Success',
                                    text: 'Needs assessment submitted successfully',
                                    icon: 'success',
                                    button: 'Ok'
                                })
                            })
                        }
                    }
                }
                

                

                // fetch('/needs-assessment/', {
                //     method: 'POST',
                //     headers: {
                //         'Content-Type': 'application/json',
                        
                //     },
                //     body: JSON.stringify(data)
                // })
                // .then(response => response.json())
                // .then(data => {
                //     console.log(data)
                //     if (data){
                //         // redirect to the needs assessment page
                //         history.pushState({}, null, `/needs-assessment/${data.slug}`); 
                //         document.getElementById('main').innerHTML = data.template;
                        
                //         // sweet alert
                //         swal({
                //             title: 'Success',
                //             text: 'Needs assessment submitted successfully',
                //             icon: 'success',
                //             button: 'Ok'
                //         })
                //     }
                // })
                // .catch(error => {
                //     console.log(error)
                //     needsAssessmentBtn.disabled = false;
                //     needsAssessmentBtn.innerHTML = 'Assess Needs'
                //     swal({
                //         title: 'Error',
                //         text: 'An error occured',
                //         icon: 'error',
                //         button: 'Ok'
                //     })
                // })
            })

                
            
        }
        // put functionality
        // else{
        //     console.log('PUT')
        //     needsAssessmentBtn.innerText = 'Update'
        //     let sectorSelectionValue = sectorSelection.value;
        //     if (sectorSelectionValue === 'health'){
        //         healthTypeContainer.classList.remove('hidden');
        //         healthContainer.classList.remove('hidden')
        //         schoolContainer.classList.add('hidden')
        //         schoolTypeContainer.classList.add('hidden');
            
        //     } else {
        //         healthTypeContainer.classList.add('hidden');
        //         healthContainer.classList.add('hidden')
        //         schoolContainer.classList.remove('hidden')
        //         schoolTypeContainer.classList.remove('hidden');
                
        //     }
        //     // check the value of the health type dropdown
        //     let type = needType.value;
        //     if (type === 'facility'){
        //         healthFacility.classList.remove('hidden');
        //         healthPersonnel.classList.add('hidden');
               
        //     } else {
        //         healthFacility.classList.add('hidden');
        //         healthPersonnel.classList.remove('hidden');
        //     }

        //     if (educationSectorType.value === 'dual_desk'){
        //         dualDesk.classList.remove('hidden');
        //         school.classList.add('hidden');
        //     }
        //     else if(educationSectorType.value === 'classroom'){
        //         dualDesk.classList.add('hidden');
        //         school.classList.remove('hidden');
        //     }

        //     // add event listener to sector selection dropdown
        //     sectorSelection.addEventListener('change', function(){
        //         let sectorSelectionValue = sectorSelection.value;
        //         if (sectorSelectionValue === 'health'){
        //             healthTypeContainer.classList.remove('hidden');
        //             healthContainer.classList.remove('hidden')
        //             schoolContainer.classList.add('hidden')
        //             schoolTypeContainer.classList.add('hidden');
        //             handleCheckboxChange()
        //             handleEducationCheckboxChange()

        //         } else if (sectorSelectionValue === 'education'){
        //             healthTypeContainer.classList.add('hidden');
        //             healthContainer.classList.add('hidden')
        //             schoolContainer.classList.remove('hidden')
        //             schoolTypeContainer.classList.remove('hidden');
        //             handleCheckboxChange()
        //             handleEducationCheckboxChange()
        //         }
        //     })

        //     // add event listener to health type dropdown
        //     sectorType.addEventListener('change', function(){
        //         let healthTypeValue = sectorType.value;
        //         if (healthTypeValue === 'facility'){
        //             healthFacility.classList.remove('hidden');
        //             healthPersonnel.classList.add('hidden');
        //             handleCheckboxChange()
                    
                    
        //         } else {
        //             healthFacility.classList.add('hidden');
        //             healthPersonnel.classList.remove('hidden');
        //             handleCheckboxChange()

        //         }

        //         if (educationSectorType.value === 'dual_desk'){
        //             dualDesk.classList.remove('hidden');
        //             school.classList.add('hidden');
        //             handleEducationCheckboxChange()
        //         }
        //         else if(educationSectorType.value === 'classroom'){
        //             dualDesk.classList.add('hidden');
        //             school.classList.remove('hidden');
        //             handleEducationCheckboxChange()
        //         }
        //     })

        //     handleCheckboxChange()
        //     handleEducationCheckboxChange()

        //     // get original data
        //     let originalData = {
        //         sector: needsAssessmentSector.value,
        //         type: needType.value,
        //         projectedPopulation: projectedPopulationSelect.value,
        //         facilityNumbers: {},
        //         personnelNumbers: {}
        //     }

        //     let inputs = personnelNumberContainerMain.querySelectorAll('input');
        //     inputs.forEach(input => {
        //         let personnelType = input.name.split('-')[1];
        //         originalData.personnelNumbers[personnelType] = input.value;
        //     })

        //     let facilityInputs = facilityNumbersContainerMain.querySelectorAll('input');
        //     facilityInputs.forEach(input => {
        //         let facilityType = input.name.split('-')[1];
        //         originalData.facilityNumbers[facilityType] = input.value;
        //     })

        //     if (type === 'facility'){
        //         // remove personnelNumber from original data
        //         delete originalData.personnelNumbers;
        //     }
        //     else{
        //         // remove facilityNumbers from original data
        //         delete originalData.facilityNumbers;
        //     }

        //     console.log(originalData)

        //     needsAssessmentBtn.addEventListener('click', function(){
        //         needsAssessmentBtn.innerHTML = `<span id="loading" class="loading loading-spinner loading-md text-gray-600"></span>`
        //         needsAssessmentBtn.disabled = true;
        //         let sectorSelectionValue = sectorSelection.value;
        //         let healthTypeValue = sectorType.value;
        //         let projectedPopulationValue = projectedPopulationSelect.value;
        //         let facilityNumbers = {};
        //         let personnelNumbers = {};
        //         let facilityNumberInputs = facilityNumbersContainerMain.querySelectorAll('input');
        //         let personnelNumberInputs = personnelNumberContainerMain.querySelectorAll('input');

        //         if (facilityNumberInputs.length > 0){
        //             facilityNumberInputs.forEach(input => {
        //                 let facilityType = input.name.split('-')[1];
        //                 facilityNumbers[facilityType] = input.value;
        //             });
        //         }

        //         if (personnelNumberInputs.length > 0){
        //             personnelNumberInputs.forEach(input => {
        //                 let personnelType = input.name.split('-')[1];
        //                 personnelNumbers[personnelType] = input.value;
        //             });
        //         }
        //         let data = ''

        //         // check if health type is facility or personnel
        //         if (healthTypeValue === 'facility'){
        //             // send post request to server
        //             data = {
        //                 sector: sectorSelectionValue,
        //                 type: healthTypeValue,
        //                 projectedPopulation: projectedPopulationValue,
        //                 facilityNumbers: facilityNumbers
        //             }
        //         }
        //         else{   
        //             data = {
        //                 sector: sectorSelectionValue,
        //                 type: healthTypeValue,
        //                 projectedPopulation: projectedPopulationValue,
        //                 personnelNumbers: personnelNumbers
        //             }
        //         }
                
        //         let newData = {
        //             sector: sectorSelectionValue,
        //             type: healthTypeValue,
        //             projectedPopulation: projectedPopulationValue,
        //             facilityNumbers: facilityNumbers,
        //             personnelNumbers: personnelNumbers
        //         }

        //         // remove facilityNumbers from original data if type is personnel
        //         if (healthTypeValue === 'personnel'){
        //             delete newData.facilityNumbers;
        //         }
        //         else{
        //             delete newData.personnelNumbers;
        //         }

        //         // check if data is different from original data
        //         let isDifferent = JSON.stringify(originalData) === JSON.stringify(newData);
        //         console.log(isDifferent)

            

        //         if (!isDifferent){
        //             console.log(data)
        //             fetch(`/needs-assessment/${needsAssessmentSlug.value}`, {
        //                 method: 'PUT',
        //                 headers: {
        //                     'Content-Type': 'application/json',
                            
        //                 },
        //                 body: JSON.stringify(data)
        //             })
        //             .then(response => response.json())
        //             .then(data => {
        //                 console.log(data)
        //                 if (data){
        //                     // redirect to the needs assessment page
        //                     history.pushState({}, null, `/needs-assessment/${data.slug}`);
        //                     document.getElementById('main').innerHTML = data.template;

        //                     // sweet alert
        //                     swal({
        //                         title: 'Success',
        //                         text: 'Needs assessment updated successfully',
        //                         icon: 'success',
        //                         button: 'Ok'
        //                     })
        //                 }
        //             })
        //             .catch(error => {
        //                 console.log(error)
        //                 needsAssessmentBtn.disabled = false;
        //                 needsAssessmentBtn.innerHTML = 'Update'
        //                 swal({
        //                     title: 'Error',
        //                     text: 'An error occured',
        //                     icon: 'error',
        //                     button: 'Ok'
        //                 })
        //             })
        //         }
        //         else{
        //             needsAssessmentBtn.disabled = false;
        //             needsAssessmentBtn.innerHTML = 'Update'
        //             swal({
        //                 title: 'Info',
        //                 text: 'No changes made, make changes to data to update needs assessment',
        //                 icon: 'info',
        //                 button: 'Ok'
        //             })

        //         }
        //     })





        //     // add event listener to projected population select

        //     // handle checkbox change if type is facility or personnel
        //     function handleCheckboxChange(){
        //        let originalInputData = {
        //             sector: needsAssessmentSector.value,
        //             type: needType.value,
        //             projectedPopulation: projectedPopulationSelect.value,
        //             facilityNumbers: {},
        //             personnelNumbers: {}
        //         }

        //         let inputs = personnelNumberContainerMain.querySelectorAll('input');
        //         inputs.forEach(input => {
        //             let personnelType = input.name.split('-')[1];
        //             originalInputData.personnelNumbers[personnelType] = input.value;
        //         })

        //         let facilityInputs = facilityNumbersContainerMain.querySelectorAll('input');
        //         facilityInputs.forEach(input => {
        //             let facilityType = input.name.split('-')[1];
        //             originalInputData.facilityNumbers[facilityType] = input.value;
        //         })

        //         console.log(originalInputData)
        //         if (sectorType.value === 'facility') {
        //             // if facilityNumberContainer is not empty, disable the needs assessment button
        //             let inputs = facilityNumbersContainerMain.querySelectorAll('input');
        //             let isEmpty = checkEmptyInput(inputs);
        //             needsAssessmentBtn.disabled = isEmpty;
        //             console.log(isEmpty)

        //             inputs.forEach(input => {
        //                 input.addEventListener('input', function(){
        //                     // check all input fields to see if they are empty
        //                     let isEmpty = checkEmptyInput(inputs);
        //                     needsAssessmentBtn.disabled = isEmpty;
        //                 })
        //             })

        //             // if inputs is less than 4, append corresponding skeletons to the facilityNumbersContainer
        //             if (inputs.length < 4){
        //                 for (let i = inputs.length; i < 4; i++) {
        //                     let skeleton = document.createElement('div');
        //                     skeleton.id = `skeleton-${i}`;
        //                     skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
        //                     skeleton.innerHTML = `
        //                         <span class="label-text mb-2">
        //                             <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        //                             <p class="italic">
        //                                 <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
        //                             </p>
        //                         </span>
        //                         <div class="h-10 bg-gray-300 rounded w-full"></div>
        //                     `;
        //                     facilityNumbersContainer.appendChild(skeleton);
        //                 }
        //             }

        //             // add event listener to facility checkboxes
        //             facilityCheckboxes.forEach((checkbox, index) => {
        //                 checkbox.addEventListener('change', function(e) {
        //                     // find it corresponding div and input
        //                     let div = document.getElementById(`facilityNumber-${e.target.value}`)
        //                     console.log(div)

        //                     if (!div){
        //                         let facilityType = e.target.value;
        //                         const inputFieldId = `facilityNumber-${facilityType}`;
        //                         facilityType = facilityType.charAt(0).toUpperCase() + facilityType.slice(1);
                                
        //                         const inputField = document.getElementById(inputFieldId) || document.createElement('div');
        //                         inputField.id = inputFieldId;
                                
        //                         inputField.innerHTML = `
        //                             <div class="form-control" id="facilityNumber-${e.target.value}">
        //                                 <span class="label-text mb-2">${facilityType}
        //                                     <p class="italic" style="font-style:italic">(enter number of ${facilityType}s)</p>

        //                                 <input id=${facilityType.replace(' ,', '')} value="" type="number" min="1" name=facilityNumber-${facilityType}" class="input mt-2 input-bordered w-full" />
        //                             </div>
        //                         `;
        //                         let facilityInput = inputField.querySelector(`input[id=${facilityType.replace(' ', '')}]`)

        //                         if (inputs){
        //                             inputs.forEach(input => {
                                        
        //                                 if (input.id === facilityType){
        //                                     facilityInput.value = input.value
        //                                 }
        //                                 console.log(input.id, facilityType)
        //                             })
        //                         }
        //                         // remove the corresponding skeleton
        //                         let skeleton = document.getElementById(`skeleton-${index}`);
        //                         if (skeleton){
        //                             skeleton.remove();
        //                         }

        //                         facilityNumbersContainer.appendChild(inputField);
                            
        //                     }
                                
                            
        //                     else{
        //                         console.log(e, 'unchecked')
        //                         let div = document.getElementById(`facilityNumber-${e.target.value}`)
                                
        //                         div.remove()

        //                         // add the corresponding skeleton
        //                         let skeleton = document.createElement('div');
        //                         skeleton.id = `skeleton-${index}`;
        //                         skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
        //                         skeleton.innerHTML = `
        //                             <span class="label-text mb-2">
        //                                 <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        //                                 <p class="italic">
        //                                     <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
        //                                 </p>
        //                             </span>
        //                             <div class="h-10 bg-gray-300 rounded w-full"></div>
        //                         `;
        //                         facilityNumbersContainer.appendChild(skeleton);

        //                     }

        //                     let newInputs = facilityNumbersContainer.querySelectorAll('input');
        //                     let isEmpty = checkEmptyInput(newInputs); // check if input field is empty
    
        //                     needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button
    
        //                     // add event listener to input fields to check if they are empty
        //                     newInputs.forEach(function(input){
        //                         input.addEventListener('input', function(){
        //                             // check all input fields to see if they are empty
        //                             let isEmpty = checkEmptyInput(newInputs);
        //                             needsAssessmentBtn.disabled = isEmpty;
        //                         })
        //                         console.log(input.value)
        //                         console.log(isEmpty)
        //                     })
        //                     console.log(newInputs)

        //                 })
        //             })
                    
        //         }
                    
        //         else {   
        //             // 
        //             let inputs = personnelNumberContainerMain.querySelectorAll('input');
        //             let isEmpty = checkEmptyInput(inputs);
        //             needsAssessmentBtn.disabled = isEmpty;
        //             console.log(isEmpty)

        //             inputs.forEach(input => {
        //                 input.addEventListener('input', function(){
        //                     // check all input fields to see if they are empty
        //                     let isEmpty = checkEmptyInput(inputs);
        //                     needsAssessmentBtn.disabled = isEmpty;
        //                 })
        //             })

        //              // if inputs is less than 4, append corresponding skeletons to the facilityNumbersContainer
        //             if (inputs.length < 4){
        //                 for (let i = inputs.length; i < 4; i++) {
        //                     let skeleton = document.createElement('div');
        //                     skeleton.id = `personnel-skeleton-${i}`;
        //                     skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
        //                     skeleton.innerHTML = `
        //                         <span class="label-text mb-2">
        //                             <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        //                             <p class="italic">
        //                                 <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
        //                             </p>
        //                         </span>
        //                         <div class="h-10 bg-gray-300 rounded w-full"></div>
        //                     `;
                            
        //                     personnelNumbers.appendChild(skeleton);
        //                 }
        //             }

        //             // add event listener to personnel checkboxes
        //             personnelCheckboxes.forEach((checkbox, index) => {
        //                 checkbox.addEventListener('change', function(e) {
        //                     if (e.target.checked){
                                
        //                         // find it corresponding div and input
        //                         let div = document.getElementById(`personnelNumber-${e.target.value}`)
        //                         console.log(div)

        //                         if (!div){
        //                             let personnelType = e.target.value;
        //                             const inputFieldId = `personnelNumber-${personnelType}`;
        //                             personnelType = personnelType.charAt(0).toUpperCase() + personnelType.slice(1);
                                    
        //                             const inputField = document.getElementById(inputFieldId) || document.createElement('div');
        //                             inputField.id = inputFieldId;
                                    
        //                             inputField.innerHTML = `
        //                                 <div class="form-control" id="personnelNumber-${e.target.value}">
        //                                     <span class="label-text mb-2">${personnelType}
        //                                         <p class="italic" style="font-style:italic">(enter number of ${personnelType}s)</p>

        //                                     <input id=${personnelType} value="" type="number" min="1" name="personnelNumber-${personnelType}" class="input mt-2 input-bordered w-full" />
        //                                 </div>
        //                             `;
        //                             let personnelInput = inputField.querySelector(`input[id=${personnelType}]`)

        //                             if (inputs){
        //                                 inputs.forEach(input => {
                                            
        //                                     if (input.id === personnelType){
        //                                         personnelInput.value = input.value
        //                                     }
        //                                     console.log(input.id, personnelType)
        //                                 })
        //                             }
        //                             // remove the corresponding skeleton
        //                             let skeleton = document.getElementById(`personnel-skeleton-${index}`);
        //                             if (skeleton){
        //                                 skeleton.remove();
        //                             }
        //                             console.log('INDEX',index)
        //                             personnelNumbers.appendChild(inputField);
                                
        //                         }
                                
        //                     }
        //                     else{
        //                         console.log(e, 'unchecked')
        //                         let div = document.getElementById(`personnelNumber-${e.target.value}`)
                                
        //                         div.remove()
        //                         // add the corresponding skeleton
        //                         let skeleton = document.createElement('div');
        //                         skeleton.id = `personnel-skeleton-${index}`;
        //                         skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
        //                         skeleton.innerHTML = `
        //                             <span class="label-text mb-2">
        //                                 <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        //                                 <p class="italic">
        //                                     <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
        //                                 </p>
        //                             </span>
        //                             <div class="h-10 bg-gray-300 rounded w-full"></div>
        //                         `;
        //                         personnelNumbers.appendChild(skeleton);

        //                     }

        //                     let newInputs = personnelNumberContainerMain.querySelectorAll('input');
        //                     let isEmpty = checkEmptyInput(newInputs); // check if input field is empty
    
        //                     needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button
    
        //                     // add event listener to input fields to check if they are empty
        //                     newInputs.forEach(function(input){
        //                         input.addEventListener('input', function(){
        //                             // check all input fields to see if they are empty
        //                             let isEmpty = checkEmptyInput(newInputs);
        //                             needsAssessmentBtn.disabled = isEmpty;
        //                         })
        //                         console.log(input.value)
        //                         console.log(isEmpty)
        //                     })
        //                     console.log(newInputs)

                            
        //                 })
        //             })
        //         }
                                    
        //     }

        //     function handleEducationCheckboxChange(){
        //         if (educationSectorType.value){
        //             console.log("EDU", educationSectorType.value)
        //             if (educationSectorType.value === 'dual_desk') {
        //                 // if facilityNumberContainer is not empty, disable the needs assessment button
        //                 let inputs = dualDeskNumbers.querySelectorAll('input');
        //                 console.log(inputs)
        //                 let isEmpty = checkEmptyInput(inputs);
        //                 needsAssessmentBtn.disabled = isEmpty;
        //                 console.log(isEmpty)
                        
        //                 // add event listener to facility checkboxes
        //                 dualDeskCheckboxes.forEach((checkbox, index) =>{
        //                     checkbox.addEventListener('change', function(e){
        //                         console.log(e.target.value)
        //                         let dualDeskType = e.target.value;
        //                         const inputFieldId = `${dualDeskType}`;
        //                         dualDeskType = dualDeskType.charAt(0).toUpperCase() + dualDeskType.slice(1);
                    
        //                         let inputField = document.createElement('div');
        //                         inputField.id = inputFieldId;
                    
        //                         if (e.target.checked) {
        //                             inputField.innerHTML = `
        //                                 <div class="form-control">
        //                                     <span class="label-text mb-2">${dualDeskType}
        //                                         <p class="italic" style="font-style:italic">(enter number of ${dualDeskType}s)</p>

        //                                     <input id=${dualDeskType.replace(' ', '')} value="" type="number" min="1" name="dualDeskNumber-${dualDeskType}" class="input mt-2 input-bordered w-full" />
        //                                 </div>

        //                             `;
        //                             // Remove the corresponding skeleton
        //                             const skeleton = document.querySelector(`#dualDeskSkeleton-${index}`);

        //                             if (skeleton) {
        //                                 skeleton.remove();
        //                             }

        //                             dualDeskNumbers.appendChild(inputField);
        //                         }
        //                         else {
        //                             const existingInputField = document.getElementById(inputFieldId);
        //                             if (existingInputField) {
        //                                 existingInputField.remove();
                                        
        //                                 // Re-add the corresponding skeleton
        //                                 let skeleton = document.createElement('div');
        //                                 skeleton.id = `dualDeskSkeleton-${index}`;
        //                                 skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
        //                                 skeleton.innerHTML = `
        //                                     <span class="label-text mb-2">
        //                                         <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        //                                         <p class="italic">
        //                                             <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
        //                                         </p>
        //                                     </span>
        //                                     <div class="h-10 bg-gray-300 rounded w-full"></div>
        //                                 `;

        //                                 dualDeskNumbers.appendChild(skeleton);
        //                             }
        //                         }
        //                         let newInputs = dualDeskNumbers.querySelectorAll('input');
        //                         let isEmpty = checkEmptyInput(newInputs); // check if input field is empty

        //                         needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button

        //                         // add event listener to input fields to check if they are empty
        //                         console.log(newInputs)
        //                         newInputs.forEach(input =>{
        //                             input.addEventListener('input', function(){
        //                                 // check all input fields to see if they are empty
        //                                 let isEmpty = checkEmptyInput(newInputs);
        //                                 needsAssessmentBtn.disabled = isEmpty;
        //                             })
        //                         })

        //                     })
        //                 })
        //             }
        //             else{
        //                 let inputs = schoolNumbers.querySelectorAll('input');
        //                 let isEmpty = checkEmptyInput(inputs);
        //                 needsAssessmentBtn.disabled = isEmpty;
        //                 console.log(isEmpty)
        //                 schoolCheckboxes.forEach((checkbox, index) =>{
        //                     checkbox.addEventListener('change', function(e){
        //                         let schoolType = e.target.value;
        //                         const inputFieldId = `${schoolType}`;
        //                         schoolType = schoolType.charAt(0).toUpperCase() + schoolType.slice(1);
                    
        //                         const inputField = document.createElement('div');
        //                         inputField.id = inputFieldId;
                    
        //                         if (e.target.checked) {
        //                             inputField.innerHTML = `
        //                                 <div class="form-control">
        //                                     <span class="label-text mb-2">${schoolType}
        //                                         <p class="italic" style="font-style:italic">(enter number of ${schoolType}s)
        //                                         </p>

        //                                     <input id=${schoolType.replace(' ', '')} value="" type="number" min="1" name="schoolNumber-${schoolType}" class="input mt-2 input-bordered w-full" />
        //                                 </div>
        //                             `;
        //                             // Remove the corresponding skeleton
        //                             const skeleton = document.querySelector(`#schoolSkeleton-${index}`);

        //                             if (skeleton) {
        //                                 skeleton.remove();
        //                             }

        //                             // append input field if it is not contained in the schoolNumbers container
        //                             const existingInputField = document.getElementById(inputFieldId);
        //                             if (!existingInputField) {
        //                                 schoolNumbers.appendChild(inputField);
        //                             }

        //                         }
        //                         else {
        //                             const existingInputField = document.getElementById(inputFieldId);
        //                             if (existingInputField) {
        //                                 existingInputField.remove();
                                        
        //                                 // Re-add the corresponding skeleton
        //                                 let skeleton = document.createElement('div');
        //                                 skeleton.id = `schoolSkeleton-${index}`;
        //                                 skeleton.classList.add('form-control', 'animate-pulse', 'mt-4');
        //                                 skeleton.innerHTML = `
        //                                     <span class="label-text mb-2">
        //                                         <div class="h-4 bg-gray-300 rounded w-3/4"></div>
        //                                         <p class="italic">
        //                                             <div class="h-3 bg-gray-300 rounded w-1/2 mt-1"></div>
        //                                         </p>
        //                                     </span>
        //                                     <div class="h-10 bg-gray-300 rounded w-full"></div>
        //                                 `;
        //                                 schoolNumbers.appendChild(skeleton);
        //                             }
        //                         }
        //                         let newInputs = schoolNumbers.querySelectorAll('input');
        //                         let isEmpty = checkEmptyInput(newInputs); // check if input field is empty

        //                         needsAssessmentBtn.disabled = isEmpty; // disable or enable the needs assessment button

        //                         // add event listener to input fields to check if they are empty
        //                         console.log(newInputs)
        //                         newInputs.forEach(input =>{
        //                             input.addEventListener('input', function(){
        //                                 // check all input fields to see if they are empty
        //                                 let isEmpty = checkEmptyInput(newInputs);
        //                                 needsAssessmentBtn.disabled = isEmpty;
        //                             })
        //                         })

        //                     })
        //                 })

        //             }
        //         }

        //     }

            
        // }

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