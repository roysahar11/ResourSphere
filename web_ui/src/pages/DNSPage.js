// File: src/pages/DNSPage.js

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
  CircularProgress,
  IconButton,
  Alert,
  Snackbar
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import api from '../services/api';

function DNSPage() {
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedZone, setSelectedZone] = useState(null);
  const [newZoneName, setNewZoneName] = useState('');
  const [actionInProgress, setActionInProgress] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchZones();
  }, []);

  const fetchZones = async () => {
    setLoading(true);
    try {
      const response = await api.listDNSZones();
      setZones(response.zones || []);
    } catch (error) {
      console.error('Failed to fetch DNS zones:', error);
      showNotification('Failed to fetch DNS zones', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateZone = async () => {
    if (!newZoneName) {
      showNotification('Please enter a zone name', 'error');
      return;
    }

    // Ensure zone name ends with a dot
    const zoneName = newZoneName.endsWith('.') ? newZoneName : `${newZoneName}.`;

    setActionInProgress(true);
    try {
      await api.createDNSZone(zoneName);
      showNotification('DNS zone created successfully', 'success');
      setCreateDialogOpen(false);
      setNewZoneName('');
      fetchZones();
    } catch (error) {
      console.error('Failed to create DNS zone:', error);
      showNotification('Failed to create DNS zone: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleDeleteZone = async () => {
    setActionInProgress(true);
    try {
      await api.deleteDNSZone(selectedZone.zone_id);
      showNotification(`DNS zone ${selectedZone.name} deleted successfully`, 'success');
      setDeleteDialogOpen(false);
      fetchZones();
    } catch (error) {
      console.error('Failed to delete DNS zone:', error);
      showNotification('Failed to delete DNS zone: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setActionInProgress(false);
    }
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

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          DNS Zones
        </Typography>
        <Box>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />} 
            onClick={fetchZones}
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
            Create Zone
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
                <TableCell>Zone Name</TableCell>
                <TableCell>Zone ID</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {zones.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No DNS zones found. Create one to get started.
                  </TableCell>
                </TableRow>
              ) : (
                zones.map((zone) => (
                  <TableRow key={zone.zone_id}>
                    <TableCell>{zone.name}</TableCell>
                    <TableCell>{zone.zone_id}</TableCell>
                    <TableCell align="right">
                      <IconButton 
                        color="error" 
                        onClick={() => {
                          setSelectedZone(zone);
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

      {/* Create Zone Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)}>
        <DialogTitle>Create DNS Zone</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ mb: 2 }}>
            Enter a domain name for your new DNS zone (e.g., example.com).
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Domain Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newZoneName}
            onChange={(e) => setNewZoneName(e.target.value)}
            placeholder="example.com"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleCreateZone} 
            variant="contained" 
            disabled={actionInProgress}
          >
            {actionInProgress ? <CircularProgress size={24} /> : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete DNS Zone</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the DNS zone "{selectedZone?.name}"? 
            This action cannot be undone and all DNS records will be permanently deleted.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleDeleteZone} 
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

export default DNSPage;