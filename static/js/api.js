class API {
    constructor(csrfToken) {
        this.csrfToken = csrfToken;
    }

    send(endPoint, data, readyFunction) {
        // Create XMLHttpRequest object
        const xhr = new XMLHttpRequest();
        xhr.open('POST', "/" + endPoint, true);
        xhr.setRequestHeader('X-CSRFToken', this.csrfToken);
        xhr.onreadystatechange = readyFunction;
        xhr.send(data);
    }
}