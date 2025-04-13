import React from 'react';
import { Admin, Resource, ListGuesser, EditGuesser, ShowGuesser } from 'react-admin';
import dataProvider from './dataProvider';

const AdminDashboard = () => (
    <Admin dataProvider={dataProvider}>
        <Resource name="users" list={ListGuesser} edit={EditGuesser} show={ShowGuesser} />
    </Admin>
);

export default AdminDashboard;
