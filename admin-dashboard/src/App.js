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
  useCreate,
  useDataProvider, // Import useDataProvider
  BulkDeleteWithConfirmButton,
} from "react-admin";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Menu,
  MenuItem, 
  ListItemIcon,
  ListItemText,
  Button,
  Divider,
  useTheme,
  Switch,
  FormControlLabel,
  TextField as MuiTextField,
  Paper,
  Link,
  CircularProgress,
  Select, 
  InputLabel, 
  FormControl, 
} from "@mui/material";
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
// import RefreshIcon from '@mui/icons-material/Refresh'; // REMOVED: RefreshIcon is no longer needed
import { 
    Dialog, // MUI Dialog
    DialogActions, // MUI DialogActions
    DialogContent, // MUI DialogContent
    DialogContentText, // MUI DialogContentText
    DialogTitle,// MUI DialogTitle
} from "@mui/material";
import './App.css';


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
                const error = await response.json();
                throw new Error(error.message || `Failed to fetch ${resource}/${params.id}`);
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
// Replace your existing Dashboard component with this updated version

const Dashboard = () => {
    const theme = useTheme();
    const [metrics, setMetrics] = useState({
        job_seekers: 0,
        companies: 0,
        jobs: 0,
        applications: 0
    });
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            setError(null);
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout for faster initial load
            
            const response = await fetch(`${API_BASE_URL}/dashboard`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            const transformedMetrics = {
                job_seekers: data.metrics?.users || data.metrics?.job_seekers || 0,
                companies: data.metrics?.companies || 0,
                jobs: data.metrics?.jobs || 0,
                applications: data.metrics?.applications || 0
            };
            
            setMetrics(transformedMetrics);
            setChartData(data.trends?.map(item => ({ 
                x: item.x, 
                applications: item.applications, 
                registrations: item.logins 
            })) || []);
            
        } catch (error) {
            console.error("Error fetching dashboard data:", error);
            setError(error.message);
            
            // Set default values on error
            setMetrics({
                job_seekers: 0,
                companies: 0,
                jobs: 0,
                applications: 0
            });
            setChartData([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // Immediate data fetch on component mount
        fetchDashboardData();
        
        // Set up auto-refresh every 30 seconds
        const intervalId = setInterval(fetchDashboardData, 30000);
        
        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
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

    // Show loading state only for initial load
    if (loading && Object.values(metrics).every(val => val === 0)) {
        return (
            <Box p={3} display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <Box textAlign="center">
                    <CircularProgress size={40} />
                    <Typography variant="body1" sx={{ mt: 1 }}>
                        Loading...
                    </Typography>
                </Box>
            </Box>
        );
    }

    // Show error state with retry option
    if (error && Object.values(metrics).every(val => val === 0)) {
        return (
            <Box p={3} display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                <Box textAlign="center">
                    <Typography variant="h6" color="error" sx={{ mb: 2 }}>
                        Failed to load dashboard data
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                        {error}
                    </Typography>
                    <Button 
                        variant="contained" 
                        onClick={fetchDashboardData}
                        disabled={loading}
                    >
                        {loading ? 'Retrying...' : 'Retry'}
                    </Button>
                </Box>
            </Box>
        );
    }

    return (
        <Box p={3}>
            {/* Add refresh indicator */}
            {loading && (
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                    <CircularProgress size={20} />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                        Refreshing...
                    </Typography>
                </Box>
            )}
            
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
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h6" sx={{ color: 'text.primary' }}>
                        Activity Trends
                    </Typography>
                    <Button 
                        size="small" 
                        onClick={fetchDashboardData}
                        disabled={loading}
                        sx={{ textTransform: 'none' }}
                    >
                        {loading ? 'Refreshing...' : 'Refresh'}
                    </Button>
                </Box>
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
                                backgroundColor: theme.palette.background.paper,
                                color: theme.palette.text.primary,
                                borderRadius: '8px',
                                borderColor: theme.palette.divider,
                                boxShadow: theme.shadows[3],
                            }}
                            cursor={{ stroke: theme.palette.action.hover, strokeWidth: 2 }}
                        />
                        <Legend 
                            wrapperStyle={{ paddingTop: 20 }}
                            iconSize={16}
                            iconType="circle"
                        />
                        <Line 
                            type="monotone" 
                            dataKey="applications"
                            name="Applications"
                            stroke={theme.palette.primary.main} 
                            strokeWidth={2}
                            activeDot={{ r: 6 }}
                            dot={{ r: 3 }}
                        />
                        <Line 
                            type="monotone" 
                            dataKey="registrations" 
                            name="Registrations"
                            stroke="#388e3c"
                            strokeWidth={2}
                            activeDot={{ r: 6 }}
                            dot={{ r: 3 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </Box>
        </Box>
    );
};


// This component displays details in a popup.
// Fixed DetailsDialog component with better alignment
const DetailsDialog = ({ open, onClose, title, data, loading, fieldsOrder }) => {
    // Helper to format keys (e.g., 'company_name' -> 'Company Name')
    const formatLabel = (key) => {
        if (key === 'is_banned') return 'Ban Status';
        return key
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    };

    // Helper to format values
    const formatValue = (key, value) => {
        if (typeof value === 'boolean') {
            return value ? 'Yes' : 'No';
        }
        if (value === null || value === undefined || value === '') {
            return 'N/A';
        }
        // Special formatting for created_at if it's a date string
        if (key === 'created_at' && typeof value === 'string' && !isNaN(new Date(value))) {
            return new Date(value).toLocaleDateString() + ' ' + new Date(value).toLocaleTimeString();
        }
        return String(value);
    };

    const displayData = {};
    if (data && fieldsOrder) {
        fieldsOrder.forEach(key => {
            if (data.hasOwnProperty(key)) {
                displayData[key] = data[key];
            }
        });
    } else if (data) {
        // Fallback if no fieldsOrder is provided, but still filter out some
        Object.entries(data).forEach(([key, value]) => {
            if (key === 'id' || key === 'login_id' || key.endsWith('_picture') || key === 'logo' || key === 'description' || key === 'about_me') {
                return; // Skip non-display fields and specific removals
            }
            displayData[key] = value;
        });
    }

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" scroll="paper">
            <DialogTitle>{title}</DialogTitle>
            <DialogContent dividers>
                {loading && (
                    <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                        <CircularProgress />
                    </Box>
                )}
                {!loading && data && (
                    <Box sx={{ mt: 1 }}>
                        {Object.entries(displayData).map(([key, value]) => (
                            <Box 
                                key={key} 
                                sx={{ 
                                    display: 'flex',
                                    flexDirection: { xs: 'column', sm: 'row' },
                                    mb: 2,
                                    minHeight: 'auto'
                                }}
                            >
                                <Box sx={{ 
                                    minWidth: { xs: 'auto', sm: 120 },
                                    maxWidth: { xs: 'none', sm: 120 },
                                    mr: { xs: 0, sm: 2 },
                                    mb: { xs: 0.5, sm: 0 },
                                    flexShrink: 0
                                }}>
                                    <Typography 
                                        variant="subtitle2" 
                                        color="text.secondary" 
                                        fontWeight="bold"
                                        sx={{ 
                                            fontSize: '0.875rem',
                                            lineHeight: 1.2
                                        }}
                                    >
                                        {formatLabel(key)}
                                    </Typography>
                                </Box>
                                <Box sx={{ flex: 1, minWidth: 0 }}>
                                    <Typography 
                                        variant="body2" 
                                        sx={{ 
                                            wordBreak: 'break-word',
                                            fontSize: '0.875rem',
                                            lineHeight: 1.4
                                        }}
                                    >
                                        {formatValue(key, value)}
                                    </Typography>
                                </Box>
                            </Box>
                        ))}
                    </Box>
                )}
                {!loading && !data && (
                    <Typography variant="body1" sx={{ p: 4, textAlign: 'center' }}>
                        No details available.
                    </Typography>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
};

// ClickableNameField Component
const ClickableNameField = ({ source, resource }) => {
    const record = useRecordContext();
    const dataProvider = useDataProvider();
    const [open, setOpen] = useState(false);
    const [details, setDetails] = useState(null);
    const [loading, setLoading] = useState(false);
    const notify = useNotify();

    if (!record) return null;

    const handleClick = (event) => {
        event.stopPropagation(); // Stop row click event
        event.preventDefault();
        setOpen(true);
        setLoading(true);

        // Fetch the full details of the record
        dataProvider.getOne(resource, { id: record.id })
            .then(({ data }) => {
                setDetails(data);
                setLoading(false);
            })
            .catch(error => {
                setLoading(false);
                setOpen(false);
                notify(`Error fetching details: ${error.message}`, { type: 'error' });
            });
    };

    const handleClose = () => {
        setOpen(false);
        setDetails(null); // Reset details for next open
    };

    const dialogTitle = resource === 'users' ? record.name || 'Job Seeker Details' : record.company_name || 'Company Details';

    // Define the specific display order and filter for each resource
    let fieldsOrder = [];
    if (resource === 'users') {
        fieldsOrder = ['age', 'email', 'phone', 'college_name', 'about_me', 'is_banned', 'created_at'];
    } else if (resource === 'companies') {
        fieldsOrder = ['email', 'address', 'industry', 'description', 'website', 'is_banned', 'created_at'];
    }

    return (
        <>
            <Link
                component="button"
                variant="body2"
                onClick={handleClick}
                sx={{ 
                    textAlign: 'left', 
                    textTransform: 'none', 
                    textDecoration: 'none', // Remove underline
                    color: 'primary.main', // Keep the primary color to indicate it's clickable
                    // cursor: 'pointer', '&:hover': { textDecoration: 'underline' } // Optional: add underline on hover for better UX 
                }}
            >
                {record[source]}
            </Link>
            <DetailsDialog
                open={open}
                onClose={handleClose}
                title={dialogTitle}
                data={details}
                loading={loading}
                fieldsOrder={fieldsOrder} // Pass the specific order
            />
        </>
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
                    { label: "Company", value: "company:", icon: <FactoryIcon /> },
                    { label: "Job Type", value: "job_type:", icon: <CategoryIcon /> },
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

const industryOptions = [
  "Agriculture, Forestry, and Fishing",
  "Mining and Quarrying",
  "Manufacturing",
  "Electricity, Gas, Steam, and Air Conditioning Supply",
  "Water Supply; Sewerage, Waste Management, and Remediation Activities",
  "Construction",
  "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
  "Transportation and Storage",
  "Accommodation and Food Service Activities",
  "Information and Communication",
  "Financial and Insurance Activities",
  "Real Estate Activities",
  "Professional, Scientific, and Technical Activities",
  "Administrative and Support Service Activities",
  "Public Administration and Defence; Compulsory Social Security",
  "Education",
  "Human Health and Social Work Activities",
  "Arts, Entertainment, and Recreation",
  "Other Service Activities",
  "Activities of Households as Employers",
  "Activities of Extraterritorial Organizations and Bodies"
];

const AddCompanyDialog = ({ open, handleClose }) => {
  const [create] = useCreate();
  const notify = useNotify();
  const refresh = useRefresh();
  const dataProvider = useDataProvider(); // Add this hook for checking existing companies

  const [formData, setFormData] = useState({
    company_name: '',
    email: '',
    address: '',
    website: '',
    logo: '',
    description: '',
    industry: '', // Default to empty string for initial selection
    password: '',
  });

  const [passwordError, setPasswordError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [companyNameError, setCompanyNameError] = useState('');
  const [isCheckingCompany, setIsCheckingCompany] = useState(false); // Loading state for company check

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (e.target.name === 'password') {
      setPasswordError('');
    } else if (e.target.name === 'email') {
      setEmailError('');
    } else if (e.target.name === 'company_name') {
      setCompanyNameError('');
    }
  };

  const validatePassword = (password) => {
    if (password.includes(' ')) {
      return 'Password cannot contain spaces.';
    }
    if (!/^[a-zA-Z0-9@#$%^&+=]+$/.test(password)) {
      return 'Password can only contain letters, numbers, and special characters @#$%^&+=';
    }
    if (password.length < 8) {
      return 'Password must be at least 8 characters long.';
    }
    return '';
  };

  const validateEmail = (email) => {
    if (!email) {
      return 'Email address is required.';
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return 'Please enter a valid email address.';
    }
    return '';
  };

  const validateCompanyName = (companyName) => {
    if (!companyName) {
      return 'Company Name is required.';
    }
    return '';
  };

  // New function to check if company name already exists
  const checkCompanyNameExists = async (companyName) => {
    try {
      const { data } = await dataProvider.getList('companies', {
        pagination: { page: 1, perPage: 1000 }, // Adjust perPage as needed
        sort: { field: 'id', order: 'ASC' },
        filter: {}
      });
      
      // Check if company name exists (case-insensitive)
      return data.some(company => 
        company.company_name.toLowerCase() === companyName.toLowerCase()
      );
    } catch (error) {
      console.error('Error checking company name:', error);
      throw new Error('Unable to verify company name. Please try again.');
    }
  };

  const handleSubmit = async () => {
    const passwordValidationMessage = validatePassword(formData.password);
    const emailValidationMessage = validateEmail(formData.email);
    const companyNameValidationMessage = validateCompanyName(formData.company_name);

    if (passwordValidationMessage) {
      setPasswordError(passwordValidationMessage);
    }
    if (emailValidationMessage) {
      setEmailError(emailValidationMessage);
    }
    if (companyNameValidationMessage) {
      setCompanyNameError(companyNameValidationMessage);
    }

    if (passwordValidationMessage || emailValidationMessage || companyNameValidationMessage) {
      return;
    }

    // Check if company name already exists
    setIsCheckingCompany(true);
    try {
      const companyExists = await checkCompanyNameExists(formData.company_name);
      
      if (companyExists) {
        setCompanyNameError('A company with this name already exists. Please choose a different name.');
        setIsCheckingCompany(false);
        return;
      }
    } catch (error) {
      setIsCheckingCompany(false);
      notify(`Error: ${error.message}`, { type: 'error' });
      return;
    }
    setIsCheckingCompany(false);

    try {
      const dataToCreate = {
        ...formData,
        is_banned: false,
      };

      await create('companies', { data: dataToCreate });
      notify('Company added successfully!', { type: 'success' });
      refresh();
      handleClose();
      setFormData({
        company_name: '',
        email: '',
        address: '',
        website: '',
        logo: '',
        description: '',
        industry: '',
        password: '',
      });
      setPasswordError('');
      setEmailError('');
      setCompanyNameError('');
    } catch (error) {
      notify(`Error adding company: ${error.message}`, { type: 'error' });
      console.error("Error adding company:", error);
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle>Add New Company</DialogTitle>
      <DialogContent>
        <DialogContentText sx={{ mb: 2 }}>
          Please fill in the details for the new company.
        </DialogContentText>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <MuiTextField
              autoFocus
              margin="dense"
              name="company_name"
              label="Company Name"
              type="text"
              fullWidth
              variant="outlined"
              value={formData.company_name}
              onChange={handleChange}
              required
              error={!!companyNameError}
              helperText={companyNameError}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <MuiTextField
              margin="dense"
              name="email"
              label="Email Address"
              type="email"
              fullWidth
              variant="outlined"
              value={formData.email}
              onChange={handleChange}
              required
              error={!!emailError}
              helperText={emailError}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <MuiTextField
              margin="dense"
              name="password"
              label="Password"
              type="password"
              fullWidth
              variant="outlined"
              value={formData.password}
              onChange={handleChange}
              error={!!passwordError}
              helperText={passwordError || "Must be at least 8 characters and contain letters, numbers, or @#$%^&+="}
              required
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth margin="dense" variant="outlined">
              <InputLabel id="industry-label">Industry</InputLabel>
              <Select
                labelId="industry-label"
                id="industry"
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                label="Industry"
              >
                <MenuItem value="">
                  <em>None</em>
                </MenuItem>
                {industryOptions.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <MuiTextField
              margin="dense"
              name="address"
              label="Address"
              type="text"
              fullWidth
              multiline
              rows={2}
              variant="outlined"
              value={formData.address}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <MuiTextField
              margin="dense"
              name="website"
              label="Website"
              type="url"
              fullWidth
              variant="outlined"
              value={formData.website}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <MuiTextField
              margin="dense"
              name="logo"
              label="Logo URL"
              type="url"
              fullWidth
              variant="outlined"
              value={formData.logo}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <MuiTextField
              margin="dense"
              name="description"
              label="Description"
              type="text"
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              value={formData.description}
              onChange={handleChange}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          Cancel
        </Button>
        <Button 
          onClick={handleSubmit} 
          color="primary" 
          variant="contained"
          disabled={isCheckingCompany}
        >
          {isCheckingCompany ? 'Checking...' : 'Add Company'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const AddCompanyButton = () => {
  const theme = useTheme();
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Button
        startIcon={<AddIcon />}
        onClick={handleClickOpen}
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
      <AddCompanyDialog open={open} handleClose={handleClose} />
    </>
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
        rowClick="edit" // NOTE: This can be removed if you only want click interaction on the name field
    >
        {children}
    </Datagrid>
);

const BanToggle = ({ record, resource }) => {
    const [update, { isLoading }] = useUpdate();
    const notify = useNotify();
    const theme = useTheme();
    const refresh = useRefresh();

    
    const [isBanned, setIsBanned] = useState(!!record.is_banned); // !! converts to boolean

    
    useEffect(() => {
        setIsBanned(!!record.is_banned);
    }, [record.is_banned]); 

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
                    refresh(); 
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

// =============================================================================
// == UPDATED UserList COMPONENT ==
// =============================================================================
const UserList = (props) => (
    <List 
        actions={<ListActions />}
        filters={[
            <SearchInput 
                source="q" 
                alwaysOn 
                placeholder="Search job seekers..." 
                sx={{ maxWidth: 400 }}
            />
        ]} 
        {...props}
    >
        <StyledDatagrid bulkActionButtons={<UserBulkActionButtons />} rowClick={false}>
            {/* <TextField source="id" sortable={false} /> */}
            {/* MODIFIED: Replaced TextField with our new ClickableNameField */}
            <FunctionField
                label="Name"
                sortBy="name"
                render={() => <ClickableNameField source="name" resource="users" />}
            />
            <TextField source="email" />
            <TextField source="college_name" label="College" />
            <FunctionField
                label="Ban Status"
                render={(record) => <BanToggle record={record} resource="users" />}
            />
        </StyledDatagrid>
    </List>
);

// =============================================================================
// == UPDATED CompanyList COMPONENT ==
// =============================================================================
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
        <StyledDatagrid bulkActionButtons={<CompanyBulkActionButtons />} rowClick={false}>
            {/* <TextField source="id" /> */}
            {/* MODIFIED: Replaced TextField with our new ClickableNameField */}
             <FunctionField
                label="Company Name"
                sortBy="company_name"
                render={() => <ClickableNameField source="company_name" resource="companies" />}
            />
            <TextField source="email" />
            <TextField source="industry" sortable={false} />
            <FunctionField
                label="Ban Status"
                render={(record) => <BanToggle record={record} resource="companies" />}
            />
        </StyledDatagrid>
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
                sx={{ maxWidth: 500 }}
            />
        ]} 
        {...props}
    >
        <StyledDatagrid bulkActionButtons={<JobBulkActionButtons />}>
            {/* <TextField source="id" sortable={false} /> */}
            <TextField
                source="title"
                render={(params) => (
                    <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                        {params.record.title}
                    </Typography>
                )}
            />
            <TextField 
                source="company_name" 
                label="Company"
                sortable={false}
                render={(params) => (
                    <Typography variant="body2" sx={{ color: 'primary.main' }}>
                        {params.record.company_name}
                    </Typography>
                )}
            />
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
    <Admin 
        dataProvider={customDataProvider} 
        authProvider={authProvider}
        dashboard={Dashboard}
        loginPage={CustomLoginPage}
        layout={CustomLayout}
        title="Admin Portal"
    >
        <Resource name="users" list={UserList} options={{ label: 'Job Seekers' }} />
        <Resource name="companies" list={CompanyList} />
        <Resource name="jobs" list={JobList} />
    </Admin>
);

export default App;
