import { fetchUtils } from 'react-admin';

const API_URL = 'http://127.0.0.1:5000'; // Flask server

const httpClient = (url, options = {}) => {
    options.headers = new Headers({ 'Content-Type': 'application/json' });
    return fetchUtils.fetchJson(url, options);
};

const dataProvider = {
    getList: (resource, params) => {
        return httpClient(`${API_URL}/${resource}`).then(({ json }) => ({
            data: json,
            total: json.length,
        }));
    },
    getOne: (resource, params) =>
        httpClient(`${API_URL}/${resource}/${params.id}`).then(({ json }) => ({
            data: json,
        })),
    create: (resource, params) =>
        httpClient(`${API_URL}/${resource}`, {
            method: 'POST',
            body: JSON.stringify(params.data),
        }).then(({ json }) => ({ data: json })),
    delete: (resource, params) =>
        httpClient(`${API_URL}/${resource}/${params.id}`, {
            method: 'DELETE',
        }).then(() => ({ data: params.previousData })),
};

export default dataProvider;
