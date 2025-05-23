import * as React from "react";
import { 
  Admin, 
  Resource, 
  List, 
  Datagrid, 
  TextField,
  SearchInput,
  TopToolbar,
  FunctionField,
  ExportButton,
  useListContext,
  BooleanField,
  BooleanInput,
  useUpdate,
  useNotify
} from "react-admin";
import { Card, CardContent, Typography, Grid, Box, Menu, MenuItem, ListItemIcon, ListItemText, Button, Divider, useTheme, Switch, FormControlLabel } from "@mui/material";
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import LocationOnIcon from '@mui/icons-material/LocationOn';
import WorkIcon from '@mui/icons-material/Work';
import BusinessIcon from '@mui/icons-material/Business';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import LanguageIcon from '@mui/icons-material/Language';
import HomeIcon from '@mui/icons-material/Home';
import FilterListIcon from '@mui/icons-material/FilterList';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import CorporateFareIcon from '@mui/icons-material/CorporateFare';
import WorkOutlineIcon from '@mui/icons-material/WorkOutline';
import AssignmentIcon from '@mui/icons-material/Assignment';
import AddIcon from '@mui/icons-material/Add';
import BlockIcon from '@mui/icons-material/Block';
import BadgeIcon from '@mui/icons-material/Badge';
import CategoryIcon from '@mui/icons-material/Category';
import EventIcon from '@mui/icons-material/Event';
import FactoryIcon from '@mui/icons-material/Factory';
import LockIcon from '@mui/icons-material/Lock';

// Import the auth provider
import authProvider from './auth/authProvider';

const API_BASE_URL = 'http://127.0.0.1:5000';

const customDataProvider = {
    getList: async (resource, params) => {
        try {
            let url = `${API_BASE_URL}/${resource}`;
            if (params.filter && Object.keys(params.filter).length > 0) {
                const queryParams = new URLSearchParams();
                Object.entries(params.filter).forEach(([key, value]) => {
                    if (value) {
                        queryParams.append(key, value);
                    }
                });
                if (queryParams.toString()) {
                    url += `?${queryParams.toString()}`;
                }
            }
            
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch ${resource}`);
            }

            const json = await response.json();
            const formattedData = json.map(item => ({
                id: item.id || item.job_id || item.company_id,
                ...item
            }));

            return { data: formattedData, total: formattedData.length };
        } catch (error) {
            console.error("Error fetching data:", error);
            return { data: [], total: 0 };
        }
    },

    getOne: async (resource, params) => {
        try {
            const response = await fetch(`${API_BASE_URL}/${resource}/${params.id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch ${resource}/${params.id}`);
            }

            const data = await response.json();
            return { data: { ...data, id: params.id } };
        } catch (error) {
            console.error("Error fetching item:", error);
            throw error;
        }
    },

    create: async (resource, params) => {
        try {
            const response = await fetch(`${API_BASE_URL}/${resource}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(params.data),
            });

            if (!response.ok) {
                throw new Error(`Failed to create ${resource}`);
            }

            const data = await response.json();
            return { data: { ...data, id: data.id || data.job_id || data.company_id } };
        } catch (error) {
            console.error("Error creating item:", error);
            throw error;
        }
    },

    update: async (resource, params) => {
        try {
            const response = await fetch(`${API_BASE_URL}/${resource}/${params.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(params.data),
            });

            if (!response.ok) {
                throw new Error(`Failed to update ${resource}/${params.id}`);
            }

            const data = await response.json();
            return { data: { ...data, id: params.id } };
        } catch (error) {
            console.error("Error updating item:", error);
            throw error;
        }
    },

    delete: async (resource, params) => {
        try {
            const response = await fetch(`${API_BASE_URL}/${resource}/${params.id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(`Failed to delete ${resource}/${params.id}`);
            }

            return { data: { id: params.id } };
        } catch (error) {
            console.error("Error deleting item:", error);
            throw error;
        }
    },
    
     deleteMany: async (resource, params) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/${resource}/bulk`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ ids: params.ids }),
            });

            if (!response.ok) {
                throw new Error(`Failed to delete ${resource} items`);
            }

            return { data: params.ids };
        } catch (error) {
            console.error("Delete many error:", error);
            throw error;
        }
    },
};

const metricIcons = {
    users: <PeopleAltIcon sx={{ fontSize: 40, color: 'white' }} />,
    companies: <CorporateFareIcon sx={{ fontSize: 40, color: 'white' }} />,
    jobs: <WorkOutlineIcon sx={{ fontSize: 40, color: 'white' }} />,
    applications: <AssignmentIcon sx={{ fontSize: 40, color: 'white' }} />
};

const Dashboard = () => {
    const theme = useTheme();
    const [metrics, setMetrics] = useState({
        users: 0,
        companies: 0,
        jobs: 0,
        applications: 0
    });

    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetch(`${API_BASE_URL}/dashboard`)
            .then((res) => res.json())
            .then((data) => {
                setMetrics(data.metrics);
                setChartData(data.trends.map(item => ({ 
                    x: item.x, 
                    applications: item.applications, 
                    logins: item.logins 
                })));
            })
            .catch((error) => console.error("Error fetching dashboard data:", error));
    }, []);

    const metricColors = [
        theme.palette.primary.main,
        theme.palette.secondary.main,
        '#4caf50',
        '#9c27b0'
    ];

    return (
        <Box p={3}>
            <Grid container spacing={3}>
                {Object.entries(metrics).map(([key, value], index) => (
                    <Grid item xs={12} sm={6} md={3} key={key}>
                        <Card elevation={3} sx={{ 
                            background: metricColors[index],
                            color: 'white',
                            borderRadius: 3,
                            overflow: 'visible',
                            '&:hover': { transform: 'translateY(-4px)', transition: 'transform 0.3s' }
                        }}>
                            <CardContent>
                                <Box display="flex" justifyContent="space-between" alignItems="center">
                                    <div>
                                        <Typography variant="subtitle2" sx={{ opacity: 0.9, letterSpacing: 1 }}>
                                            {key.replace("_", " ").toUpperCase()}
                                        </Typography>
                                        <Typography variant="h3" sx={{ fontWeight: 700, mt: 1 }}>
                                            {value}
                                        </Typography>
                                    </div>
                                    <Box sx={{
                                        bgcolor: 'rgba(255,255,255,0.2)',
                                        p: 1.5,
                                        borderRadius: 3
                                    }}>
                                        {metricIcons[key]}
                                    </Box>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Divider sx={{ my: 4, bgcolor: 'divider', height: 2 }} />

            <Box sx={{ 
                height: 400,
                bgcolor: 'background.paper',
                borderRadius: 3,
                p: 3,
                boxShadow: 1
            }}>
                <Typography variant="h6" sx={{ mb: 3, color: 'text.primary' }}>
                    Activity Trends
                </Typography>
                <ResponsiveContainer width="100%" height="90%">
                    <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
                        <XAxis 
                            dataKey="x" 
                            label={{ 
                                value: "Date", 
                                position: "bottom",
                                offset: 0,
                                fill: theme.palette.text.secondary
                            }}
                            tick={{ fill: theme.palette.text.secondary }}
                        />
                        <YAxis 
                            label={{ 
                                value: "Activity", 
                                angle: -90, 
                                position: "left",
                                fill: theme.palette.text.secondary
                            }}
                            tick={{ fill: theme.palette.text.secondary }}
                        />
                        <Tooltip 
                            contentStyle={{
                                borderRadius: 8,
                                borderColor: theme.palette.divider,
                                boxShadow: theme.shadows[3]
                            }}
                        />
                        <Legend 
                            wrapperStyle={{ paddingTop: 20 }}
                            iconSize={16}
                            iconType="circle"
                        />
                        <Line 
                            type="monotone" 
                            dataKey="applications" 
                            stroke={theme.palette.primary.main} 
                            strokeWidth={2}
                            dot={{ fill: theme.palette.primary.main }}
                        />
                        <Line 
                            type="monotone" 
                            dataKey="logins" 
                            stroke={theme.palette.secondary.main} 
                            strokeWidth={2}
                            dot={{ fill: theme.palette.secondary.main }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </Box>
        </Box>
    );
};

const FilterDropdown = () => {
    const { resource, filterValues, setFilters } = useListContext();
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const theme = useTheme();
    
    const handleClick = (event) => setAnchorEl(event.currentTarget);
    const handleClose = () => setAnchorEl(null);
    
    const applyFilter = (filter) => {
        setFilters({ ...filterValues, q: filter });
        handleClose();
    };
    
    const getFilterOptions = () => {
        switch(resource) {
            case 'users':
                return [
                    { label: "Name", value: "name:", icon: <PersonIcon /> },
                    { label: "Email", value: "email:", icon: <EmailIcon /> }
                ];
            case 'companies':
                return [
                    { label: "Company Name", value: "company_name:", icon: <BusinessIcon /> },
                    { label: "Email", value: "email:", icon: <EmailIcon /> },
		    { label: "Industry", value: "industry:", icon: <FactoryIcon /> }
                ];
            case 'jobs':
                return [
                    { label: "Title", value: "title:", icon: <WorkIcon /> },
                    { label: "Company", value: "created_by:", icon: <FactoryIcon /> },
                    { label: "Date Posted", value: "created_at:", icon: <EventIcon /> },
                    { label: "Status", value: "status:", icon: <LockIcon /> }
                ];
            default:
                return [];
        }
    };

    const filterOptions = getFilterOptions();
    
    return filterOptions.length > 0 && (
        <>
            <Button
                startIcon={<FilterListIcon />}
                onClick={handleClick}
                variant="contained"
                size="medium"
                sx={{ 
                    mr: 2,
                    borderRadius: 20,
                    textTransform: 'none',
                    px: 3,
                    bgcolor: theme.palette.background.paper,
                    color: theme.palette.text.primary,
                    '&:hover': {
                        bgcolor: theme.palette.action.hover
                    }
                }}
            >
                Filter By
            </Button>
            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                PaperProps={{ 
                    sx: { 
                        borderRadius: 3,
                        mt: 1,
                        boxShadow: 3
                    } 
                }}
            >
                {filterOptions.map((option) => (
                    <MenuItem 
                        key={option.value} 
                        onClick={() => applyFilter(option.value)}
                        sx={{ py: 1.5, minWidth: 200 }}
                    >
                        <ListItemIcon sx={{ minWidth: 40 }}>
                            {React.cloneElement(option.icon, { 
                                sx: { color: theme.palette.text.secondary } 
                            })}
                        </ListItemIcon>
                        <ListItemText 
                            primary={option.label} 
                            primaryTypographyProps={{ variant: 'body2' }}
                        />
                    </MenuItem>
                ))}
            </Menu>
        </>
    );
};

const AddCompanyButton = () => {
    const theme = useTheme();
    
    const handleAddCompany = () => {
        window.location.href = 'http://localhost:5000/company/company_profile';
    };
    
    return (
        <Button
            startIcon={<AddIcon />}
            onClick={handleAddCompany}
            variant="contained"
            color="primary"
            size="medium"
            sx={{ 
                ml: 2,
                borderRadius: 20,
                textTransform: 'none',
                px: 3
            }}
        >
            Add Company
        </Button>
    );
};

const ListActions = (props) => {
    const { resource } = props;
    
    return (
        <TopToolbar {...props} sx={{ p: 2, bgcolor: 'background.default' }}>
            <FilterDropdown />
            <ExportButton 
                sx={{ 
                    borderRadius: 20,
                    textTransform: 'none',
                    px: 3,
                    '&:hover': { bgcolor: 'action.hover' }
                }}
            />
            {resource === 'companies' && <AddCompanyButton />}
        </TopToolbar>
    );
};

const StyledDatagrid = ({ children, ...props }) => (
    <Datagrid
        {...props}
        sx={{
            '& .RaDatagrid-headerCell': {
                bgcolor: 'background.default',
                fontWeight: 700,
            },
            '& .RaDatagrid-rowCell': {
                py: 2,
            },
            '& .RaDatagrid-row:hover': {
                bgcolor: 'action.hover'
            }
        }}
        rowClick="edit"
    >
        {children}
    </Datagrid>
);

const BanToggle = ({ record, resource }) => {
    const [update, { isLoading }] = useUpdate();
    const notify = useNotify();
    const theme = useTheme();
    
    const [isBanned, setIsBanned] = useState(record.is_banned || false);
    
    const handleToggle = (event) => {
        const newValue = event.target.checked;
        setIsBanned(newValue);
        
        update(
            resource,
            { id: record.id, data: { is_banned: newValue }, previousData: record },
            {
                onSuccess: () => {
                    notify(
                        newValue ? 'User has been banned' : 'User has been unbanned',
                        { type: 'success' }
                    );
                },
                onError: (error) => {
                    setIsBanned(!newValue);
                    notify(
                        `Error: Couldn't update ban status - ${error.message}`,
                        { type: 'error' }
                    );
                }
            }
        );
    };
    
    return (
        <FormControlLabel
            control={
                <Switch
                    checked={isBanned}
                    onChange={handleToggle}
                    disabled={isLoading}
                    color="error"
                    size="small"
                />
            }
            label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {isBanned && (
                        <BlockIcon 
                            fontSize="small" 
                            sx={{ mr: 0.5, color: theme.palette.error.main }}
                        />
                    )}
                    <Typography variant="body2">
                        {isBanned ? "Banned" : "Ban"}
                    </Typography>
                </Box>
            }
            sx={{ m: 0 }}
        />
    );
};

const UserList = (props) => (
    <List 
        actions={<ListActions />}
        filters={[
            <SearchInput 
                source="q" 
                alwaysOn 
                placeholder="Search users..." 
                sx={{ maxWidth: 400 }}
            />
        ]} 
        {...props}
    >
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
            <TextField source="email" />
            <FunctionField
                label="Ban Status"
                render={(record) => <BanToggle record={record} resource="users" />}
            />
        </Datagrid>
    </List>
);

const CompanyList = (props) => (
    <List 
        actions={<ListActions resource="companies" />}
        filters={[
            <SearchInput 
                source="q" 
                alwaysOn 
                placeholder="Search companies..." 
                sx={{ maxWidth: 400 }}
            />
        ]}
        {...props}
    >
        <Datagrid>
            <TextField source="id" />
            <TextField source="company_name" />
            <TextField source="email" />
            <FunctionField
                label="Ban Status"
                render={(record) => <BanToggle record={record} resource="companies" />}
            />
        </Datagrid>
    </List>
);
const JobList = (props) => (
    <List 
        actions={<ListActions />}
        filters={[
            <SearchInput 
                source="q" 
                alwaysOn 
                placeholder="Search jobs..." 
                sx={{ maxWidth: 400 }}
            />
        ]}
        {...props}
    >
        <StyledDatagrid>  <TextField source="id" />
            <TextField source="title" />
            <TextField source="description" />
            <TextField source="job_type" />
            <TextField source="location" />
            <TextField source="salary" />
            <TextField source="total_vacancy" />
            <TextField source="filled_vacancy" />
            <TextField source="status" />
        </StyledDatagrid>
    </List>
);

const App = () => (
    <Admin dataProvider={customDataProvider} dashboard={Dashboard}>
        <Resource name="users" list={UserList} />
        <Resource name="companies" list={CompanyList} />
        <Resource name="jobs" list={JobList} />
    </Admin>
);

export default App;
