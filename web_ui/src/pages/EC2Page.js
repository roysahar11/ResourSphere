// File: src/pages/EC2Page.js

import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
  MenuItem,
  CircularProgress,
  Chip,
  IconButton,
  Alert,
  Snackbar
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  PlayArrow as StartIcon,
  Stop as StopIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function EC2Page() {
  const { userPermissions } = useAuth();
  const [instances, setInstances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedInstance, setSelectedInstance] = useState(null);
  const [newInstanceName, setNewInstanceName] = useState('');
  const [selectedInstanceType, setSelectedInstanceType] = useState('');
  const [selectedAmi, setSelectedAmi] = useState('');
  const [actionInProgress, setActionInProgress] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchInstances();
  }, []);

  const fetchInstances = async () => {
    setLoading(true);
    try {
      const instances = await api.listEC2Instances();
      setInstances(instances);
    } catch (error) {
      console.error('Failed to fetch instances:', error);
      showNotification('Failed to fetch instances', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateInstance = async () => {
    if (!newInstanceName || !selectedInstanceType || !selectedAmi) {
      showNotification('Please fill all required fields', 'error');
      return;
    }

    setActionInProgress(true);
    try {
      await api.createEC2Instance(newInstanceName, selectedInstanceType, selectedAmi);
      showNotification('Instance created successfully', 'success');
      setCreateDialogOpen(false);
      resetCreateForm();
      fetchInstances();
    } catch (error) {
      console.error('Failed to create instance:', error);
      showNotification('Failed to create instance: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleStartInstance = async (instance) => {
    setActionInProgress(true);
    try {
      await api.startEC2Instance(instance.instance_id);
      showNotification(`Instance ${instance.name} started successfully`, 'success');
      fetchInstances();
    } catch (error) {
      console.error('Failed to start instance:', error);
      showNotification('Failed to start instance', 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleStopInstance = async (instance) => {
    setActionInProgress(true);
    try {
      await api.stopEC2Instance(instance.instance_id);
      showNotification(`Instance ${instance.name} stopped successfully`, 'success');
      fetchInstances();
    } catch (error) {
      console.error('Failed to stop instance:', error);
      showNotification('Failed to stop instance', 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleDeleteInstance = async () => {
    setActionInProgress(true);
    try {
      await api.deleteEC2Instance(selectedInstance.instance_id);
      showNotification(`Instance ${selectedInstance.name} deleted successfully`, 'success');
      setDeleteDialogOpen(false);
      fetchInstances();
    } catch (error) {
      console.error('Failed to delete instance:', error);
      showNotification('Failed to delete instance', 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const resetCreateForm = () => {
    setNewInstanceName('');
    setSelectedInstanceType('');
    setSelectedAmi('');
  };

  const showNotification = (message, severity) => {
    setNotification({
      open: true,
      message,
      severity
    });
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const getStateColor = (state) => {
    switch (state) {
      case 'running':
        return 'success';
      case 'stopped':
        return 'error';
      case 'pending':
      case 'stopping':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          EC2 Instances
        </Typography>
        <Box>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />} 
            onClick={fetchInstances}
            sx={{ mr: 2 }}
            disabled={loading || actionInProgress}
          >
            Refresh
          </Button>
          <Button 
            variant="contained" 
            startIcon={<AddIcon />} 
            onClick={() => setCreateDialogOpen(true)}
            disabled={loading || actionInProgress}
          >
            Create Instance
          </Button>
        </Box>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Instance ID</TableCell>
                <TableCell>Public IP</TableCell>
                <TableCell>State</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {instances.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    No instances found. Create one to get started.
                  </TableCell>
                </TableRow>
              ) : (
                instances.map((instance) => (
                  <TableRow key={instance.instance_id}>
                    <TableCell>{instance.name}</TableCell>
                    <TableCell>{instance.instance_id}</TableCell>
                    <TableCell>{instance.public_ip}</TableCell>
                    <TableCell>
                      <Chip 
                        label={instance.state} 
                        color={getStateColor(instance.state)} 
                        size="small" 
                      />
                    </TableCell>
                    <TableCell align="right">
                      {instance.state === 'stopped' && (
                        <IconButton 
                          color="success" 
                          onClick={() => handleStartInstance(instance)}
                          disabled={actionInProgress}
                        >
                          <StartIcon />
                        </IconButton>
                      )}
                      {instance.state === 'running' && (
                        <IconButton 
                          color="warning" 
                          onClick={() => handleStopInstance(instance)}
                          disabled={actionInProgress}
                        >
                          <StopIcon />
                        </IconButton>
                      )}
                      <IconButton 
                        color="error" 
                        onClick={() => {
                          setSelectedInstance(instance);
                          setDeleteDialogOpen(true);
                        }}
                        disabled={actionInProgress}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Create Instance Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)}>
        <DialogTitle>Create EC2 Instance</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ mb: 2 }}>
            Configure your new EC2 instance.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Instance Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newInstanceName}
            onChange={(e) => setNewInstanceName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            select
            margin="dense"
            id="instanceType"
            label="Instance Type"
            fullWidth
            variant="outlined"
            value={selectedInstanceType}
            onChange={(e) => setSelectedInstanceType(e.target.value)}
            sx={{ mb: 2 }}
          >
            {userPermissions?.ec2_instance_types.map((type) => (
              <MenuItem key={type} value={type}>
                {type}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            margin="dense"
            id="ami"
            label="AMI"
            fullWidth
            variant="outlined"
            value={selectedAmi}
            onChange={(e) => setSelectedAmi(e.target.value)}
          >
            {Object.entries(userPermissions?.ami_choice || {}).map(([key, value]) => (
              <MenuItem key={key} value={key}>
                {key} ({value})
              </MenuItem>
            ))}
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleCreateInstance} 
            variant="contained" 
            disabled={actionInProgress}
          >
            {actionInProgress ? <CircularProgress size={24} /> : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Instance</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the instance "{selectedInstance?.name}"? 
            This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleDeleteInstance} 
            color="error" 
            variant="contained"
            disabled={actionInProgress}
          >
            {actionInProgress ? <CircularProgress size={24} /> : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Notification Snackbar */}
      <Snackbar 
        open={notification.open} 
        autoHideDuration={6000} 
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity} 
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default EC2Page;