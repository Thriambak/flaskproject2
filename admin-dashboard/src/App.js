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
  defaultTheme,
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
  Chip,
  List as MuiList,
  ListItem,
  ListItemAvatar,
  Avatar,
} from "@mui/material";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import AddBusinessIcon from '@mui/icons-material/AddBusiness';
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
import SchoolIcon from '@mui/icons-material/School';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import PostAddIcon from '@mui/icons-material/PostAdd';
import SendIcon from '@mui/icons-material/Send';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
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
    sessionStorage.removeItem('redirected'); // Clear refresh flag on logout
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
        const isAuthenticated = localStorage.getItem('isAuthenticated');

        if (isAuthenticated) {
            // If authenticated, clear any refresh flag and proceed
            sessionStorage.removeItem('redirected');
            return Promise.resolve();
        }

        // If not authenticated, check if we've already tried to refresh this session
        const hasRefreshed = sessionStorage.getItem('redirected');

        if (!hasRefreshed) {
            // If we haven't refreshed yet, set the flag and reload the page once
            sessionStorage.setItem('redirected', 'true');
            window.location.reload();
            // Return a pending promise to prevent the app from rendering briefly
            return new Promise(() => {}); 
        }

        // If we have already refreshed, reject to trigger the normal login redirect
        return Promise.reject();
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

// <<< CREATE A DEDICATED LIGHT THEME FOR THE LOGIN PAGE >>>
const loginPageTheme = createTheme({
  ...defaultTheme,
  palette: {
    ...defaultTheme.palette,
    mode: 'light', // This forces the light mode
  },
});

// Custom Login Page Component
const CustomLoginPage = () => {
    // We get the theme from the outer context for the background gradient
    const theme = useTheme(); 
    
    return (
        // <<< WRAP THE ENTIRE PAGE IN THE LIGHT THEME PROVIDER >>>
        <ThemeProvider theme={loginPageTheme}>
            <Box
                sx={{
                    minHeight: '100vh',
                    // Use the specific color values for the gradient
                    background: `linear-gradient(135deg, ${loginPageTheme.palette.primary.main} 0%, ${loginPageTheme.palette.secondary.main} 100%)`,
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
                        // Force a light background for the paper component
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        backdropFilter: 'blur(10px)'
                    }}
                >
                    <Box sx={{ textAlign: 'center', mb: 3 }}>
                        <AdminPanelSettingsIcon 
                            sx={{ 
                                fontSize: 60, 
                                color: 'primary.main', // This will now correctly use the light theme's primary color
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
        </ThemeProvider>
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

// Recent Activity Feed Component
const RecentActivityFeed = () => {
    const theme = useTheme();
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch recent activities - you'll need to create this endpoint
        fetch(`${API_BASE_URL}/recent-activities`)
            .then((res) => res.json())
            .then((data) => {
                setActivities(data.slice(0, 10)); // Show only last 10 activities
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching recent activities:", error);
                setLoading(false);
            });
    }, []);

    const getActivityIcon = (type) => {
        switch(type) {
            case 'user_registration':
                return <PersonAddIcon sx={{ color: theme.palette.primary.main }} />;
            case 'company_registration':
                return <AddBusinessIcon sx={{ color: theme.palette.secondary.main }} />;
            case 'job_posting':
                return <PostAddIcon sx={{ color: theme.palette.success.main }} />;
            case 'application_submission':
                return <SendIcon sx={{ color: theme.palette.info.main }} />;
            default:
                return <EventIcon sx={{ color: theme.palette.text.secondary }} />;
        }
    };

    const formatActivityText = (activity) => {
        switch(activity.type) {
            case 'user_registration':
                return `${activity.user_name} registered as a job seeker`;
            case 'company_registration':
                return `${activity.company_name} registered as a company`;
            case 'job_posting':
                return `${activity.company_name} posted a new job: ${activity.job_title}`;
            case 'application_submission':
                return `${activity.user_name} applied for ${activity.job_title}`;
            default:
                return activity.description || 'Unknown activity';
        }
    };

    const formatTimeAgo = (timestamp) => {
        const now = new Date();
        const time = new Date(timestamp);
        const diffInMinutes = Math.floor((now - time) / (1000 * 60));
        
        if (diffInMinutes < 1) return 'Just now';
        if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
        if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
        return `${Math.floor(diffInMinutes / 1440)}d ago`;
    };

    if (loading) {
        return (
            <Card sx={{ height: 400 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>Recent Activity</Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
                        <CircularProgress />
                    </Box>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card sx={{ height: 400, overflow: 'hidden' }}>
            <CardContent sx={{ p: 0, height: '100%' }}>
                <Box sx={{ p: 3, pb: 1 }}>
                    <Typography variant="h6" gutterBottom>Recent Activity</Typography>
                </Box>
                <MuiList sx={{ height: 'calc(100% - 80px)', overflow: 'auto', p: 0 }}>
                    {activities.length === 0 ? (
                        <ListItem>
                            <Typography variant="body2" color="text.secondary">
                                No recent activities found
                            </Typography>
                        </ListItem>
                    ) : (
                        activities.map((activity, index) => (
                            <ListItem key={index} sx={{ py: 1.5, px: 3 }}>
                                <ListItemAvatar>
                                    <Avatar sx={{ bgcolor: 'transparent', width: 32, height: 32 }}>
                                        {getActivityIcon(activity.type)}
                                    </Avatar>
                                </ListItemAvatar>
                                <Box sx={{ flex: 1, minWidth: 0 }}>
                                    <Typography 
                                        variant="body2" 
                                        sx={{ 
                                            mb: 0.5,
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            display: '-webkit-box',
                                            WebkitLineClamp: 2,
                                            WebkitBoxOrient: 'vertical',
                                        }}
                                    >
                                        {formatActivityText(activity)}
                                    </Typography>
                                    <Typography variant="caption" color="text.secondary">
                                        {formatTimeAgo(activity.timestamp)}
                                    </Typography>
                                </Box>
                            </ListItem>
                        ))
                    )}
                </MuiList>
            </CardContent>
        </Card>
    );
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
                    registrations: item.logins 
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

            <Grid container spacing={3}>
                {/* Activity Trends Chart */}
                <Grid item xs={12} md={8}>
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
                                    stroke="#388e3c" // A distinct, theme-friendly green
                                    strokeWidth={2}
                                    activeDot={{ r: 6 }}
                                    dot={{ r: 3 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </Box>
                </Grid>

                {/* Recent Activity Feed */}
                <Grid item xs={12} md={4}>
                    <RecentActivityFeed />
                </Grid>
            </Grid>
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

// Job Status Visual Indicator Component
const JobStatusIndicator = ({ status }) => {
    const getStatusProps = (status) => {
        switch(status?.toLowerCase()) {
            case 'open':
                return {
                    color: 'success',
                    icon: <CheckCircleIcon sx={{ fontSize: 16 }} />,
                    label: 'Open'
                };
            case 'closed':
                return {
                    color: 'error',
                    icon: <CancelIcon sx={{ fontSize: 16 }} />,
                    label: 'Closed'
                };
            case 'paused':
                return {
                    color: 'warning',
                    icon: <HourglassEmptyIcon sx={{ fontSize: 16 }} />,
                    label: 'Paused'
                };
            default:
                return {
                    color: 'default',
                    icon: <HourglassEmptyIcon sx={{ fontSize: 16 }} />,
                    label: status || 'Unknown'
                };
        }
    };

    const statusProps = getStatusProps(status);

    return (
        <Chip
            icon={statusProps.icon}
            label={statusProps.label}
            color={statusProps.color}
            variant="outlined"
            size="small"
            sx={{ 
                fontWeight: 600,
                '& .MuiChip-icon': {
                    marginLeft: '8px'
                }
            }}
        />
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
                    { label: "Email", value: "email:", icon: <EmailIcon /> },
                    { label: "College", value: "college_name:", icon: <SchoolIcon /> }
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
    const dataProvider = useDataProvider();
    const theme = useTheme();

    const [formData, setFormData] = useState({ company_name: '', email: '', address: '', website: '', logo: '', description: '', industry: '', password: '' });
    const [passwordError, setPasswordError] = useState('');
    const [emailError, setEmailError] = useState('');
    const [companyNameError, setCompanyNameError] = useState('');
    const [isCheckingCompany, setIsCheckingCompany] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        if (name === 'password') setPasswordError('');
        if (name === 'email') setEmailError('');
        if (name === 'company_name') setCompanyNameError('');
    };

    const validatePassword = (password) => {
        if (password.includes(' ')) return 'Password cannot contain spaces.';
        if (!/^[a-zA-Z0-9@#$%^&+=]+$/.test(password)) return 'Password can only contain letters, numbers, and @#$%^&+=';
        if (password.length < 8) return 'Password must be at least 8 characters long.';
        return '';
    };

    const validateEmail = (email) => {
        if (!email) return 'Email address is required.';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Please enter a valid email address.';
        return '';
    };

    const validateCompanyName = (companyName) => {
        if (!companyName) return 'Company Name is required.';
        return '';
    };

    const checkCompanyNameExists = async (companyName) => {
        try {
            const { data } = await dataProvider.getList('companies', { pagination: { page: 1, perPage: 1000 }, sort: { field: 'id', order: 'ASC' }, filter: {} });
            return data.some(company => company.company_name.toLowerCase() === companyName.toLowerCase());
        } catch (error) {
            console.error('Error checking company name:', error);
            throw new Error('Unable to verify company name. Please try again.');
        }
    };
    
    const resetForm = () => {
        setFormData({ company_name: '', email: '', address: '', website: '', logo: '', description: '', industry: '', password: '' });
        setPasswordError('');
        setEmailError('');
        setCompanyNameError('');
    };
    
    const handleDialogClose = () => {
        resetForm();
        handleClose();
    };

    const handleSubmit = async () => {
        const passwordValidationMessage = validatePassword(formData.password);
        const emailValidationMessage = validateEmail(formData.email);
        const companyNameValidationMessage = validateCompanyName(formData.company_name);
        if (passwordValidationMessage) setPasswordError(passwordValidationMessage);
        if (emailValidationMessage) setEmailError(emailValidationMessage);
        if (companyNameValidationMessage) setCompanyNameError(companyNameValidationMessage);
        if (passwordValidationMessage || emailValidationMessage || companyNameValidationMessage) return;

        setIsCheckingCompany(true);
        try {
            const companyExists = await checkCompanyNameExists(formData.company_name);
            if (companyExists) {
                setCompanyNameError('A company with this name already exists.');
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
            await create('companies', { data: { ...formData, is_banned: false } });
            notify('Company added successfully!', { type: 'success' });
            refresh();
            handleDialogClose();
        } catch (error) {
            notify(`Error adding company: ${error.message}`, { type: 'error' });
        }
    };

    return (
        <Dialog open={open} onClose={handleDialogClose} fullWidth maxWidth="md">
            <Box sx={{
                p: 3,
                bgcolor: 'primary.main',
                color: 'primary.contrastText',
                display: 'flex',
                alignItems: 'center',
                gap: 2
            }}>
                <AddBusinessIcon sx={{ fontSize: 40 }}/>
                <Box>
                    <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold' }}>
                        Create New Company
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.8 }}>
                        Fill out the form to register a new company profile.
                    </Typography>
                </Box>
            </Box>
            
            <DialogContent sx={{ p: 3 }}>
                {/* PRIMARY DETAILS SECTION */}
                <Box sx={{ mb: 4 }}>
                    <Typography variant="subtitle2" gutterBottom sx={{ color: 'text.secondary', fontWeight: 600, mb: 1 }}>
                        PRIMARY DETAILS
                    </Typography>
                    <Divider sx={{ mb: 3 }} />
                    
                    <Box sx={{
                        display: 'grid',
                        gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' },
                        gap: 3,
                        mb: 3
                    }}>
                        <MuiTextField 
                            autoFocus 
                            name="company_name" 
                            label="Company Name" 
                            fullWidth 
                            variant="outlined" 
                            value={formData.company_name} 
                            onChange={handleChange} 
                            required 
                            error={!!companyNameError} 
                            helperText={companyNameError} 
                        />
                        <MuiTextField 
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
                    </Box>
                    
                    <Box sx={{
                        display: 'grid',
                        gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' },
                        gap: 3
                    }}>
                        <MuiTextField 
                            name="password" 
                            label="Password" 
                            type="password" 
                            fullWidth 
                            variant="outlined" 
                            value={formData.password} 
                            onChange={handleChange} 
                            required 
                            error={!!passwordError} 
                            helperText={passwordError || "8+ characters, no spaces"} 
                        />
                        <FormControl fullWidth variant="outlined">
                            <InputLabel id="industry-label">Industry</InputLabel>
                            <Select 
                                labelId="industry-label" 
                                id="industry" 
                                name="industry" 
                                value={formData.industry} 
                                onChange={handleChange} 
                                label="Industry"
                            >
                                <MenuItem value=""><em>None</em></MenuItem>
                                {industryOptions.map((option) => (
                                    <MenuItem key={option} value={option}>{option}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Box>
                </Box>

                {/* ADDITIONAL INFORMATION SECTION */}
                <Box>
                    <Typography variant="subtitle2" gutterBottom sx={{ color: 'text.secondary', fontWeight: 600, mb: 1 }}>
                        ADDITIONAL INFORMATION
                    </Typography>
                    <Divider sx={{ mb: 3 }} />
                    
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                        <MuiTextField 
                            name="address" 
                            label="Address" 
                            fullWidth 
                            multiline 
                            rows={2} 
                            variant="outlined" 
                            value={formData.address} 
                            onChange={handleChange} 
                        />
                        
                        <Box sx={{
                            display: 'grid',
                            gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' },
                            gap: 3
                        }}>
                            <MuiTextField 
                                name="website" 
                                label="Website URL" 
                                type="url" 
                                fullWidth 
                                variant="outlined" 
                                value={formData.website} 
                                onChange={handleChange} 
                            />
                            <MuiTextField 
                                name="logo" 
                                label="Logo URL" 
                                type="url" 
                                fullWidth 
                                variant="outlined" 
                                value={formData.logo} 
                                onChange={handleChange} 
                            />
                        </Box>
                        
                        <MuiTextField 
                            name="description" 
                            label="Company Description" 
                            fullWidth 
                            multiline 
                            rows={3} 
                            variant="outlined" 
                            value={formData.description} 
                            onChange={handleChange} 
                        />
                    </Box>
                </Box>
            </DialogContent>
            
            <DialogActions sx={{ p: 3, borderTop: `1px solid ${theme.palette.divider}`, gap: 2 }}>
                <Button onClick={handleDialogClose} size="large">Cancel</Button>
                <Button 
                    onClick={handleSubmit} 
                    variant="contained" 
                    size="large"
                    disabled={isCheckingCompany} 
                    startIcon={isCheckingCompany ? <CircularProgress size={20} color="inherit" /> : <AddIcon />}
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
            <FunctionField
                label="Status"
                source="status"
                render={(record) => <JobStatusIndicator status={record.status} />}
            />
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
