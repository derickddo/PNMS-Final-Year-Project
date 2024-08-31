// document.addEventListener('DOMContentLoaded', () => {
//     const targetNode = document.getElementById('mainContent');
//     const config = { childList: true, subtree: true };

//     const callback = function(mutationsList, observer) {
//         for(let mutation of mutationsList) {
//             if (mutation.type === 'childList') {
//                 console.log('A child node has been added or removed.');
//                 handleContentChange();
//             }
//         }
//     };

//     const observer = new MutationObserver(callback);
//     observer.observe(targetNode, config);

//     function handleContentChange() {
//         console.log('Content has changed');
//         // Put your custom logic here
//     }
// });

export let  innerHTMLListener = (targetNode, handleContentChange, url) => {
    const config = { childList: true, subtree: true };

    const callback = function(mutationsList, observer) {
        for(let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                if (url) {
                    console.log('A child node has been added or removed.', url);
                    handleContentChange();
                }
            }
        }
    };

    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
}

