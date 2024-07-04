let sectorSelection = document.getElementById('sectorSelection');
let healthTypeContainer = document.getElementById('healthTypeContainer');
let needsAssessmentBtn = document.getElementById('needsAssessmentBtn');
let projectedPopulationSelect = document.getElementById('projectedPopulationSelect');
let sectorType = document.getElementById('sectorType');
const checkboxes = document.querySelectorAll('.facility-checkbox');
const facilityNumbersContainer = document.getElementById('facilityNumbers');
const facilityNumbersContainerMain = document.getElementById('facilityNumberContainer');
let inputFields = [];
let healthFacilityTypeContainer = document.getElementById('healthFacilityTypeContainer');
let hidden = document.getElementById('hidden')





let inputs = facilityNumbersContainer.querySelectorAll('input')
let inputsArray = Array.from(inputs);

// function to check if all input fields are filled
function checkInputs(inputs) {
    let allFieldsFilled = inputs.every(field => {
        return field.value !== '';
    });
    needsAssessmentBtn.disabled = !allFieldsFilled;
}

function handleEditInputFields(inputs) {
    // Add event listener to each input
    inputs.forEach(input => {
        input = document.getElementById(input.id) 
        if (input){
            input.addEventListener('input', ()=>{
                checkInputs(inputs)
                console.log(inputs)
            
            });
        }
    });

}



if (hidden.value){
    const originalData = {
        sector: sectorSelection.value,
        projectedPopulation: projectedPopulationSelect.value,
        facilityNumbers: {},
        needType: sectorType.value
    };
    inputs.forEach((input) => {
        let facilityType = input.name.split('-')[1];
        originalData.facilityNumbers[facilityType] = input.value;
    });


    let sector = sectorSelection.value;
    let editBtn = document.querySelector('.edit-need')
    let deleteBtn = document.querySelector('.delete-need')
    needsAssessmentBtn.innerText = 'Update'
    editBtn.addEventListener('click', ()=>{
        // get all fields including checked check boxes
        
        inputs.forEach((input) =>{
            input.disabled = false
        })
        sectorSelection.disabled = false
        projectedPopulationSelect.disabled = false
        sectorType.disabled = false
        checkboxes.forEach((checkbox) =>{
            checkbox.disabled = false
        })
        handleCheckBoxes(checkboxes, inputsArray)
        checkInputs(inputsArray)
        handleSectorSelection(sector)
        // Scroll smoothly to resultsContainer
        let main = document.getElementById('main');
        if (main) {
            main.scrollIntoView({ behavior: 'smooth' });
        }
         
    })

    handleEditInputFields(inputsArray)
    needsAssessmentBtn.addEventListener('click', function() {
       

        let sector = sectorSelection.value;
        let projectedPopulation = projectedPopulationSelect.value;
        let facilityNumbers = {};
        inputsArray.forEach(inputField => {
            let input = inputField;
            let facilityType = input.name.split('-')[1];
            facilityNumbers[facilityType] = input.value;
        });
        let url = '/needs-assessment/' + hidden.value
    
        let data = {
            sector,
            projectedPopulation,
            facilityNumbers,
            needType: sectorType.value
        };

        // compare the original data with the new data
        let newData = JSON.stringify(data)
        let originalDataString = JSON.stringify(originalData)
        if (newData === originalDataString){
            // sweet alert
            swal({
                title: "No changes made",
                text: "You have not made any changes to the data",
                icon: "info",
                button: "Ok",
              });

        }
        else{

            needsAssessmentBtn.innerHTML = `<span id="loading" class="loading loading-spinner loading-md text-gray-600"></span>`
            needsAssessmentBtn.disabled = true;
            fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
            ).then(response => response.json())
            .then(data => {
                console.log(data)
                history.pushState({}, '', '/needs-assessment/' + data.slug);
                needsAssessmentBtn.innerHTML = 'Update'
                document.getElementById('main').innerHTML = data.template;
                // Scroll smoothly to resultsContainer
                let resultsContainer = document.getElementById('resultsContainer');
                if (resultsContainer) {
                    resultsContainer.scrollIntoView({ behavior: 'smooth' });
                }
                // sweet alert
                swal({
                    title: "Data Updated",
                    text: "Data has been successfully updated",
                    icon: "success",
                    button: "Ok",
                })
            
            })
            .catch(error => {
                needsAssessmentBtn.innerHTML = 'Update'
                swal({
                    title: "Error",
                    text: `An error occured, please try again (${error})`,
                    icon: "error",
                    button: "Ok",
                })
            });
        }
         
    })

    deleteBtn.addEventListener('click', ()=>{
        let url = '/needs-assessment/' + hidden.value
        swal({
            title: "Are you sure?",
            text: "Once deleted, you will not be able to recover this data!",
            icon: "warning",
            buttons: true,
            dangerMode: true,
            })
            .then((willDelete) => {
                if (willDelete) {
                    fetch(url, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    ).then(response => response.json())
                    .then(data => {
                        console.log(data)
                        history.pushState({}, '', '/dashboard/');
                        document.getElementById('main').innerHTML = data.template;
                        // sweet alert
                        swal({
                            title: "Data Deleted",
                            text: "Data has been successfully deleted",
                            icon: "success",
                            button: "Ok",
                        })
                    
                    })
                    .catch(error => {
                        console.log(error);
                    });
                } 
                else {
                    swal("Your data is safe!");
                }
            });
    })
        



}
else{
    let sector = sectorSelection.value;
    handleSectorSelection(sector)
    handleInputFields();
    handleCheckBoxes(checkboxes)
    needsAssessmentBtn.addEventListener('click', function() {
        needsAssessmentBtn.innerHTML = `<span id="loading" class="loading loading-spinner loading-md text-gray-600"></span>`
        needsAssessmentBtn.disabled = true;
        let sector = sectorSelection.value;
        let projectedPopulation = projectedPopulationSelect.value;
        let facilityNumbers = {};
        let needType = sectorType.value
        inputFields.forEach(inputField => {
            let input = inputField.querySelector('input');
            let facilityType = input.name.split('-')[1];
            facilityNumbers[facilityType] = input.value;
        });
        let url = '/needs-assessment/';
    
        let data = {
            sector,
            projectedPopulation,
            facilityNumbers,
            needType
        };
        console.log(data)
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            history.pushState({}, '', '/needs-assessment/' + data.slug);
            document.getElementById('main').innerHTML = data.template;
            // Scroll smoothly to resultsContainer
            needsAssessmentBtn.innerHTML = 'Update'
            let resultsContainer = document.getElementById('resultsContainer');
            if (resultsContainer) {
                resultsContainer.scrollIntoView({ behavior: 'smooth' });
            }
            handleInputFields();

        })
        .catch(error => {
            needsAssessmentBtn.innerHTML = 'Assess Needs'
            swal({
                title: "Error",
                text: `An error occured, please try again (${error})`,
                icon: "error",
                button: "Ok",
            })
        });
    });
}





function handleSectorSelection(sector) {
    // Implement sector selection logic if needed
    if (sector === 'health') {
        healthTypeContainer.classList.remove('hidden');
        facilityNumbersContainerMain.classList.remove('hidden');
        healthFacilityTypeContainer.classList.remove('hidden');
    } else {
        healthTypeContainer.classList.add('hidden');
        facilityNumbersContainerMain.classList.add('hidden');
        healthFacilityTypeContainer.classList.add('hidden');
    }
    
    sectorSelection.addEventListener('change', function() {
        let sector = sectorSelection.value;
        if (sector === 'health') {
            healthTypeContainer.classList.remove('hidden');
            facilityNumbersContainerMain.classList.remove('hidden');
            healthFacilityTypeContainer.classList.remove('hidden');
        } else {
            healthTypeContainer.classList.add('hidden');
            facilityNumbersContainerMain.classList.add('hidden');
            healthFacilityTypeContainer.classList.add('hidden');
        }
    });
}


function handleCheckBoxes(checkboxes, inputs){
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            let facilityType = e.target.value;
            const inputFieldId = `facilityNumber-${facilityType}`;
            facilityType = facilityType.charAt(0).toUpperCase() + facilityType.slice(1);

            if (e.target.checked) {
                // Add input field
                let inputField = document.createElement('div');
                inputField.id = inputFieldId;
                inputField.innerHTML = `
                    <div class="form-control">
                        <span class="label-text mb-2">${facilityType}
                            <p class="italic" style="font-style:italic">(enter number of ${facilityType}s)</p>
                        </span>
                        <input value="" type="number" min="1" name="facilityNumber-${facilityType}" class="input input-bordered w-full" />
                    </div>
                `;
                if (inputs){
                    inputs.forEach(input => {
                        if (input.id !== 'hidden'){
                            let inputId = input.id.split('-')[1].toLowerCase()
                            let inputFieldID = inputFieldId.split('-')[1].toLowerCase()
                            if ( inputFieldID === inputId){
                                
                                inputField.querySelector('input').value = input.value
                            }
                           
                        }
                        
                    })
                    
                }
                console.log(inputs)
                facilityNumbersContainer.appendChild(inputField);
                inputFields.push(inputField);

                if (hidden.value){
                    // Add the new input element
                    inputField = inputField.querySelector('input')
                    inputField.id = inputFieldId
                    inputsArray.push(inputField);
                    checkInputs(inputsArray)
                    handleEditInputFields(inputsArray)
                }
                else{
                    handleInputFields();
                }
            } else {
                // Remove input field
                const inputField = document.getElementById(inputFieldId);
                if (inputField) {
                    facilityNumbersContainer.removeChild(inputField);
                    inputFields = inputFields.filter(field => field.id !== inputFieldId)
                    
                }
                if (hidden.value){
                    inputsArray = inputsArray.filter(field => field.id !== inputFieldId)
                    checkInputs(inputsArray)
                    handleEditInputFields(inputsArray)
                }
                else{
                    handleInputFields()
                }
            
            }
            
            
            
        });
    });   
}


function handleInputFields() {
    if (inputFields.length > 0) {
        // Disable button if no input field is filled
        inputFields.forEach(inputField => {
            let input = inputField.querySelector('input');
            input.addEventListener('input', function() {
                let allFieldsFilled = inputFields.every(field => {
                    let input = field.querySelector('input');
                    return input.value !== '';
                });
                needsAssessmentBtn.disabled = !allFieldsFilled;
            });
        });
    } else {
        needsAssessmentBtn.disabled = true;
    }
}



