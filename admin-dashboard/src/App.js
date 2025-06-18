import * as React from "react";
import { 
  Admin, 
  Resource, 
  List,
  Confirm,
  useRecordContext, 
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
  useNotify,
  Login,
  LoginForm,
  Layout,
  AppBar,
  UserMenu,
  Button as RaButton, // Alias React-Admin's Button to avoid conflict
  useRefresh, // Import useRefresh hook
  useGetList, // Import useGetList to manually trigger a fetch
} from "react-admin";
import { Card, CardContent, Typography, Grid, Box, Menu, MenuItem, ListItemIcon, ListItemText, Button, Divider, useTheme, Switch, FormControlLabel, TextField as MuiTextField, Paper } from "@mui/material";
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
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import RefreshIcon from '@mui/icons-material/Refresh'; // Import RefreshIcon
import CloseIcon from '@mui/icons-material/Close';
import { 
    Dialog, // MUI Dialog
    DialogActions, // MUI DialogActions
    DialogContent, // MUI DialogContent
    DialogContentText, // MUI DialogContentText
    DialogTitle, // MUI DialogTitle
    IconButton,
    CircularProgress,
} from "@mui/material";

const API_BASE_URL = 'http://127.0.0.1:5000';

// Authentication Provider
const authProvider = {
    login: ({ username, password }) => {
    if (username === 'admin' && password === 'admin') {
        // Store a flag or token in localStorage
        localStorage.setItem('isAuthenticated', 'true'); // Or store a token like 'myAuthToken'
        return Promise.resolve();
    }
    return Promise.reject(new Error('Invalid credentials'));
},
    logout: () => {
    localStorage.removeItem('isAuthenticated'); // Or removeItem('myAuthToken')
    return Promise.resolve();
},
    checkError: ({ status }) => {
        if (status === 401 || status === 403) {
            window.isAuthenticated = false;
            return Promise.reject();
        }
        return Promise.resolve();
    },
    checkAuth: () => {
    return localStorage.getItem('isAuthenticated') ? Promise.resolve() : Promise.reject();
    },
    getPermissions: () => Promise.resolve(),
};

// Custom User Menu with proper positioning
const CustomUserMenu = () => (
    <UserMenu 
        sx={{
            '& .MuiPopover-paper': {
                marginTop: '8px',
                transform: 'translateX(-50%) !important',
                left: '50% !important',
                right: 'auto !important',
                minWidth: '120px',
                maxWidth: '200px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                borderRadius: '8px'
            }
        }}
    />
);

// Custom AppBar with fixed positioning
const CustomAppBar = () => (
    <AppBar 
        userMenu={<CustomUserMenu />}
        sx={{
            '& .RaAppBar-toolbar': {
                paddingRight: '16px'
            },
            '& .RaAppBar-userMenu': {
                '& .MuiButtonBase-root': {
                    borderRadius: '50%',
                    padding: '8px'
                }
            }
        }}
    />
);

// Custom Layout with fixed AppBar
const CustomLayout = (props) => (
    <Layout {...props} appBar={CustomAppBar} />
);

// Custom Login Page Component
const CustomLoginPage = () => {
    const theme = useTheme();
    
    return (
        <Box
            sx={{
                minHeight: '100vh',
                background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 2
            }}
        >
            <Paper
                elevation={10}
                sx={{
                    padding: 4,
                    borderRadius: 4,
                    maxWidth: 400,
                    width: '100%',
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)'
                }}
            >
                <Box sx={{ textAlign: 'center', mb: 3 }}>
                    <AdminPanelSettingsIcon 
                        sx={{ 
                            fontSize: 60, 
                            color: theme.palette.primary.main,
                            mb: 2
                        }} 
                    />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                        Admin Portal
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Sign in to access your dashboard
                    </Typography>
                </Box>
                
                <LoginForm 
                    sx={{ justifyItems: 'center', 
                        '& .MuiTextField-root': {
                            mb: 1,
                            '& .MuiOutlinedInput-root': {
                                borderRadius: 2,
                            }
                        },
                        '& .MuiButton-root': {
                            borderRadius: 2,
                            py: 1.5,
                            textTransform: 'none',
                            fontSize: '1rem',
                            fontWeight: 600
                        }
                    }}
                />
            </Paper>
        </Box>
    );
};

const customDataProvider = {
    getList: async (resource, params) => {
        try {
            // Extract pagination parameters
            const { page, perPage } = params.pagination;
            const { field, order } = params.sort;
            
            // Build URL with pagination and sorting parameters
            let url = `${API_BASE_URL}/${resource}`;
            const queryParams = new URLSearchParams();
            
            // Add pagination parameters
            queryParams.append('page', page.toString());
            queryParams.append('per_page', perPage.toString());
            
            // Add sorting parameters if available
            if (field && order) {
                queryParams.append('sort', field);
                queryParams.append('order', order.toLowerCase());
            }
            
            // Add filter parameters
            if (params.filter && Object.keys(params.filter).length > 0) {
                Object.entries(params.filter).forEach(([key, value]) => {
                    if (value) {
                        queryParams.append(key, value);
                    }
                });
            }
            
            url += `?${queryParams.toString()}`;
            
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
            
            // Handle different response formats from your backend
            let data, total;
            
            if (Array.isArray(json)) {
                // If backend returns array directly (current format)
                // Apply client-side pagination as fallback
                const start = (page - 1) * perPage;
                const end = start + perPage;
                data = json.slice(start, end);
                total = json.length;
            } else if (json.data && json.total !== undefined) {
                // If backend returns paginated format
                data = json.data;
                total = json.total;
            } else {
                // Default fallback
                data = json;
                total = Array.isArray(json) ? json.length : 1;
            }
            
            const formattedData = data.map(item => ({
                id: item.id || item.job_id || item.company_id,
                ...item
            }));

            return { data: formattedData, total };
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
                body: JSON.stringify(params.data),
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
            const response = await fetch(`${API_BASE_URL}/${resource}/bulk`, {
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
// Updated AddCompanyDialog Component
const AddCompanyDialog = ({ open, onClose, onSuccess }) => {
    const [formData, setFormData] = useState({
        company_name: '',
        email: '',
        password: '',
        address: '',
        website: '',
        description: '',
        industry: ''
    });
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const notify = useNotify();
    const theme = useTheme();

    const handleInputChange = (field) => (event) => {
        setFormData(prev => ({
            ...prev,
            [field]: event.target.value
        }));
        // Clear error when user starts typing
        if (errors[field]) {
            setErrors(prev => ({
                ...prev,
                [field]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        
        if (!formData.company_name.trim()) {
            newErrors.company_name = 'Company name is required';
        }
        
        if (!formData.email.trim()) {
            newErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Please enter a valid email';
        }
        
        if (!formData.password.trim()) {
            newErrors.password = 'Password is required';
        } else if (formData.password.length < 6) {
            newErrors.password = 'Password must be at least 6 characters';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async () => {
        if (!validateForm()) {
            return;
        }

        setLoading(true);
        try {
            // Create company directly with all the data
            const companyResponse = await fetch(`${API_BASE_URL}/companies`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    company_name: formData.company_name,
                    email: formData.email,
                    password: formData.password, // Send password to backend
                    address: formData.address || null,
                    website: formData.website || null,
                    description: formData.description || null,
                    industry: formData.industry || null,
                }),
            });

            if (!companyResponse.ok) {
                const errorData = await companyResponse.json();
                throw new Error(errorData.message || 'Failed to create company');
            }

            notify('Company created successfully!', { type: 'success' });
            handleClose();
            onSuccess(); // Refresh the list
        } catch (error) {
            console.error('Error creating company:', error);
            notify(`Error: ${error.message}`, { type: 'error' });
        } finally {
            setLoading(false);
        }
    };

    const handleClose = () => {
        setFormData({
            company_name: '',
            email: '',
            password: '',
            address: '',
            website: '',
            description: '',
            industry: ''
        });
        setErrors({});
        setLoading(false);
        onClose();
    };

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            maxWidth="sm"
            fullWidth
            PaperProps={{
                sx: {
                    borderRadius: 3,
                    maxHeight: '90vh'
                }
            }}
        >
            <DialogTitle sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                pb: 2
            }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <BusinessIcon sx={{ mr: 1, color: theme.palette.primary.main }} />
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Add New Company
                    </Typography>
                </Box>
                <IconButton
                    onClick={handleClose}
                    disabled={loading}
                    size="small"
                >
                    <CloseIcon />
                </IconButton>
            </DialogTitle>

            <DialogContent sx={{ pt: 1 }}>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Company Name"
                            value={formData.company_name}
                            onChange={handleInputChange('company_name')}
                            error={!!errors.company_name}
                            helperText={errors.company_name}
                            disabled={loading}
                            required
                            variant="outlined"
                            sx={{ mb: 2 }}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Email"
                            type="email"
                            value={formData.email}
                            onChange={handleInputChange('email')}
                            error={!!errors.email}
                            helperText={errors.email}
                            disabled={loading}
                            required
                            variant="outlined"
                            sx={{ mb: 2 }}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Password"
                            type="password"
                            value={formData.password}
                            onChange={handleInputChange('password')}
                            error={!!errors.password}
                            helperText={errors.password}
                            disabled={loading}
                            required
                            variant="outlined"
                            sx={{ mb: 2 }}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Industry"
                            value={formData.industry}
                            onChange={handleInputChange('industry')}
                            disabled={loading}
                            variant="outlined"
                            sx={{ mb: 2 }}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Website"
                            value={formData.website}
                            onChange={handleInputChange('website')}
                            disabled={loading}
                            variant="outlined"
                            sx={{ mb: 2 }}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Address"
                            multiline
                            rows={2}
                            value={formData.address}
                            onChange={handleInputChange('address')}
                            disabled={loading}
                            variant="outlined"
                            sx={{ mb: 2 }}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <MuiTextField
                            fullWidth
                            label="Description"
                            multiline
                            rows={3}
                            value={formData.description}
                            onChange={handleInputChange('description')}
                            disabled={loading}
                            variant="outlined"
                        />
                    </Grid>
                </Grid>
            </DialogContent>

            <DialogActions sx={{ p: 3, pt: 2 }}>
                <Button
                    onClick={handleClose}
                    disabled={loading}
                    variant="outlined"
                    sx={{ 
                        borderRadius: 2,
                        textTransform: 'none',
                        px: 3
                    }}
                >
                    Cancel
                </Button>
                <Button
                    onClick={handleSubmit}
                    disabled={loading}
                    variant="contained"
                    startIcon={loading ? <CircularProgress size={16} /> : <AddIcon />}
                    sx={{ 
                        borderRadius: 2,
                        textTransform: 'none',
                        px: 3,
                        ml: 2
                    }}
                >
                    {loading ? 'Adding...' : 'Add Company'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

// Updated Company List Component
const CompanyList = () => (
    <List
        filters={[<SearchInput key="q" source="q" alwaysOn />]}
        actions={<CompanyListActions />}
        bulkActionButtons={<CompanyBulkActionButtons />}
        perPage={25}
        sort={{ field: 'id', order: 'ASC' }}
    >
        <Datagrid rowClick="edit" bulkActionButtons={<CompanyBulkActionButtons />}>
            <TextField source="id" label="ID" />
            <TextField source="company_name" label="Company Name" />
            <TextField source="email" label="Email" />
            <TextField source="industry" label="Industry" />
            <TextField source="website" label="Website" />
            <BooleanField source="is_banned" label="Banned" />
            <FunctionField
                label="Actions"
                render={() => <BanToggleButton />}
            />
        </Datagrid>
    </List>
);

const UserBulkActionButtons = () => (
    <BulkDeleteWithConfirmButton
        confirmTitle="Delete Job Seekers"
        confirmContent="Are you sure you want to delete the selected job seekers? This action cannot be undone."
    />
);

const CompanyBulkActionButtons = () => (
    <BulkDeleteWithConfirmButton
        confirmTitle="Delete Companies"
        confirmContent="Are you sure you want to delete the selected companies? This action cannot be undone."
    />
);

const JobBulkActionButtons = () => (
    <BulkDeleteWithConfirmButton
        confirmTitle="Delete Jobs"
        confirmContent="Are you sure you want to delete the selected jobs? This action cannot be undone."
    />
);

const metricIcons = {
    job_seekers: <PeopleAltIcon sx={{ fontSize: 40, color: 'white' }} />,
    companies: <CorporateFareIcon sx={{ fontSize: 40, color: 'white' }} />,
    jobs: <WorkOutlineIcon sx={{ fontSize: 40, color: 'white' }} />,
    applications: <AssignmentIcon sx={{ fontSize: 40, color: 'white' }} />
};

const Dashboard = () => {
    const theme = useTheme();
    const [metrics, setMetrics] = useState({
        job_seekers: 0,
        companies: 0,
        jobs: 0,
        applications: 0
    });

    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetch(`${API_BASE_URL}/dashboard`)
            .then((res) => res.json())
            .then((data) => {
                const transformedMetrics = {
                    job_seekers: data.metrics.users || data.metrics.job_seekers || 0,
                    companies: data.metrics.companies || 0,
                    jobs: data.metrics.jobs || 0,
                    applications: data.metrics.applications || 0
                };
                setMetrics(transformedMetrics);
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

    const formatMetricName = (key) => {
        return key === 'job_seekers' ? 'JOB SEEKERS' : key.replace("_", " ").toUpperCase();
    };

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
                                            {formatMetricName(key)}
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
                        <ListItemText primary={option.label} />
                    </MenuItem>
                ))}
            </Menu>
        </>
    );
};

// Bulk Delete Component with Confirmation
const BulkDeleteWithConfirmButton = ({ confirmTitle, confirmContent }) => {
    const [open, setOpen] = useState(false);
    const { selectedIds } = useListContext();
    const refresh = useRefresh();
    const notify = useNotify();
    const { resource } = useListContext();

    const handleClick = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const handleConfirm = async () => {
        try {
            await customDataProvider.deleteMany(resource, { ids: selectedIds });
            notify(`${selectedIds.length} items deleted successfully`, { type: 'success' });
            refresh();
            setOpen(false);
        } catch (error) {
            notify('Error deleting items', { type: 'error' });
            console.error('Delete error:', error);
        }
    };

    return (
        <>
            <Button
                onClick={handleClick}
                startIcon={<BlockIcon />}
                disabled={selectedIds.length === 0}
                variant="contained"
                color="error"
                sx={{ 
                    borderRadius: 2,
                    textTransform: 'none',
                    mr: 1
                }}
            >
                Delete Selected ({selectedIds.length})
            </Button>
            
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>{confirmTitle}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {confirmContent}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button onClick={handleConfirm} color="error" variant="contained">
                        Delete
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

// Custom List Actions with Add Company Button
const CompanyListActions = () => {
    const [addDialogOpen, setAddDialogOpen] = useState(false);
    const refresh = useRefresh();

    const handleAddSuccess = () => {
        refresh(); // Refresh the company list
    };

    return (
        <TopToolbar>
            <FilterDropdown />
            <Button
                onClick={() => setAddDialogOpen(true)}
                startIcon={<AddIcon />}
                variant="contained"
                sx={{ 
                    borderRadius: 20,
                    textTransform: 'none',
                    px: 3,
                    mr: 2
                }}
            >
                Add Company
            </Button>
            <ExportButton />
            
            <AddCompanyDialog
                open={addDialogOpen}
                onClose={() => setAddDialogOpen(false)}
                onSuccess={handleAddSuccess}
            />
        </TopToolbar>
    );
};

// Ban/Unban Company Component
const BanToggleButton = () => {
    const record = useRecordContext();
    const [update] = useUpdate();
    const notify = useNotify();
    const refresh = useRefresh();

    const handleToggle = async () => {
        try {
            await update('companies', {
                id: record.id,
                data: { is_banned: !record.is_banned }
            });
            notify(
                `Company ${record.is_banned ? 'unbanned' : 'banned'} successfully`,
                { type: 'success' }
            );
            refresh();
        } catch (error) {
            notify('Error updating company status', { type: 'error' });
        }
    };

    return (
        <Button
            onClick={handleToggle}
            variant="outlined"
            color={record.is_banned ? "success" : "error"}
            size="small"
            sx={{ textTransform: 'none' }}
        >
            {record.is_banned ? 'Unban' : 'Ban'}
        </Button>
    );
};

// Updated User Ban/Unban Toggle Component
const UserBanToggleButton = () => {
    const record = useRecordContext();
    const [update] = useUpdate();
    const notify = useNotify();
    const refresh = useRefresh();

    const handleToggle = async () => {
        try {
            await update('users', {
                id: record.id,
                data: { is_banned: !record.is_banned }
            });
            notify(
                `User ${record.is_banned ? 'unbanned' : 'banned'} successfully`,
                { type: 'success' }
            );
            refresh();
        } catch (error) {
            notify('Error updating user status', { type: 'error' });
        }
    };

    return (
        <Button
            onClick={handleToggle}
            variant="outlined"
            color={record.is_banned ? "success" : "error"}
            size="small"
            sx={{ textTransform: 'none' }}
        >
            {record.is_banned ? 'Unban' : 'Ban'}
        </Button>
    );
};

// Updated User List Component with Ban Toggle
const UserList = () => (
    <List
        filters={[<SearchInput key="q" source="q" alwaysOn />]}
        actions={
            <TopToolbar>
                <FilterDropdown />
                <ExportButton />
            </TopToolbar>
        }
        bulkActionButtons={<UserBulkActionButtons />}
        perPage={25}
        sort={{ field: 'id', order: 'ASC' }}
    >
        <Datagrid rowClick="edit" bulkActionButtons={<UserBulkActionButtons />}>
            <TextField source="id" label="ID" />
            <TextField source="name" label="Name" />
            <TextField source="email" label="Email" />
            <TextField source="phone" label="Phone" />
            <BooleanField source="is_banned" label="Banned" />
            <FunctionField
                label="Actions"
                render={() => <UserBanToggleButton />}
            />
        </Datagrid>
    </List>
);

// Updated Job List Component with Status field
const JobList = () => (
    <List
        filters={[<SearchInput key="q" source="q" alwaysOn />]}
        actions={
            <TopToolbar>
                <FilterDropdown />
                <ExportButton />
            </TopToolbar>
        }
        bulkActionButtons={<JobBulkActionButtons />}
        perPage={25}
        sort={{ field: 'id', order: 'ASC' }}
    >
        <Datagrid rowClick="edit" bulkActionButtons={<JobBulkActionButtons />}>
            <TextField source="id" label="ID" />
            <TextField source="title" label="Title" />
            <TextField source="created_by" label="Company" />
            <TextField source="location" label="Location" />
            <TextField source="salary" label="Salary" />
            <TextField source="status" label="Status" />
            <TextField source="job_type" label="Job Type" />
            <TextField source="total_vacancy" label="Total Positions" />
            <TextField source="filled_vacancy" label="Filled Positions" />
        </Datagrid>
    </List>
);
const App = () => (
    <Admin
        dataProvider={customDataProvider}
        authProvider={authProvider}
        loginPage={CustomLoginPage}
        layout={CustomLayout}
        dashboard={Dashboard}
    >
        <Resource
            name="users"
            list={UserList}
            options={{ label: 'Job Seekers' }}
            icon={PeopleAltIcon}
        />
        <Resource
            name="companies"
            list={CompanyList}
            options={{ label: 'Companies' }}
            icon={CorporateFareIcon}
        />
        <Resource
            name="jobs"
            list={JobList}
            options={{ label: 'Jobs' }}
            icon={WorkOutlineIcon}
        />
    </Admin>
);

export default App;