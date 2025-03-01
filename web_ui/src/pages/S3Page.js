// File: src/pages/S3Page.js

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
  Snackbar,
  FormControlLabel,
  Switch,
  Link
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
  Upload as UploadIcon
} from '@mui/icons-material';
import api from '../services/api';

function S3Page() {
  const [buckets, setBuckets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [selectedBucket, setSelectedBucket] = useState(null);
  const [newBucketName, setNewBucketName] = useState('');
  const [publicAccess, setPublicAccess] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [actionInProgress, setActionInProgress] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchBuckets();
  }, []);

  const fetchBuckets = async () => {
    setLoading(true);
    try {
      const buckets = await api.listS3Buckets();
      setBuckets(buckets);
    } catch (error) {
      console.error('Failed to fetch buckets:', error);
      showNotification('Failed to fetch buckets', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBucket = async () => {
    if (!newBucketName) {
      showNotification('Please enter a bucket name', 'error');
      return;
    }

    setActionInProgress(true);
    try {
      await api.createS3Bucket(newBucketName, publicAccess);
      showNotification('Bucket created successfully', 'success');
      setCreateDialogOpen(false);
      setNewBucketName('');
      setPublicAccess(false);
      fetchBuckets();
    } catch (error) {
      console.error('Failed to create bucket:', error);
      showNotification('Failed to create bucket: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleDeleteBucket = async () => {
    setActionInProgress(true);
    try {
      await api.deleteS3Bucket(selectedBucket.name);
      showNotification(`Bucket ${selectedBucket.name} deleted successfully`, 'success');
      setDeleteDialogOpen(false);
      fetchBuckets();
    } catch (error) {
      console.error('Failed to delete bucket:', error);
      showNotification('Failed to delete bucket: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setActionInProgress(false);
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUploadFile = async () => {
    if (!selectedFile) {
      showNotification('Please select a file to upload', 'error');
      return;
    }

    setActionInProgress(true);
    try {
      await api.uploadFileToS3(selectedBucket.name, selectedFile);
      showNotification(`File ${selectedFile.name} uploaded successfully`, 'success');
      setUploadDialogOpen(false);
      setSelectedFile(null);
    } catch (error) {
      console.error('Failed to upload file:', error);
      showNotification('Failed to upload file: ' + (error.response?.data?.detail || error.message), 'error');
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
          S3 Buckets
        </Typography>
        <Box>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />} 
            onClick={fetchBuckets}
            sx={{ mr: 2 }}
// File: src/pages/S3Page.js (continued)
            // File: src/pages/S3Page.js (continued)
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
            Create Bucket
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
                <TableCell>Bucket Name</TableCell>
                <TableCell>URL</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {buckets.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No buckets found. Create one to get started.
                  </TableCell>
                </TableRow>
              ) : (
                buckets.map((bucket) => (
                  <TableRow key={bucket.name}>
                    <TableCell>{bucket.name}</TableCell>
                    <TableCell>
                      <Link href={bucket.url} target="_blank" rel="noopener">
                        {bucket.url}
                      </Link>
                    </TableCell>
                    <TableCell align="right">
                      <IconButton 
                        color="primary" 
                        onClick={() => {
                          setSelectedBucket(bucket);
                          setUploadDialogOpen(true);
                        }}
                        disabled={actionInProgress}
                      >
                        <UploadIcon />
                      </IconButton>
                      <IconButton 
                        color="error" 
                        onClick={() => {
                          setSelectedBucket(bucket);
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

      {/* Create Bucket Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)}>
        <DialogTitle>Create S3 Bucket</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ mb: 2 }}>
            Enter a name for your new S3 bucket. Bucket names must be globally unique.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Bucket Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newBucketName}
            onChange={(e) => setNewBucketName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <FormControlLabel
            control={
              <Switch
                checked={publicAccess}
                onChange={(e) => setPublicAccess(e.target.checked)}
                color="primary"
              />
            }
            label="Make bucket publicly accessible"
          />
          {publicAccess && (
            <Alert severity="warning" sx={{ mt: 2 }}>
              Making a bucket public allows anyone to access its contents. Only use this for content that should be publicly available.
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleCreateBucket} 
            variant="contained" 
            disabled={actionInProgress}
          >
            {actionInProgress ? <CircularProgress size={24} /> : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Bucket</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the bucket "{selectedBucket?.name}"? 
            This action cannot be undone and all contents will be permanently deleted.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleDeleteBucket} 
            color="error" 
            variant="contained"
            disabled={actionInProgress}
          >
            {actionInProgress ? <CircularProgress size={24} /> : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Upload File Dialog */}
      <Dialog open={uploadDialogOpen} onClose={() => setUploadDialogOpen(false)}>
        <DialogTitle>Upload File to {selectedBucket?.name}</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ mb: 2 }}>
            Select a file to upload to this bucket.
          </DialogContentText>
          <input
            accept="*/*"
            style={{ display: 'none' }}
            id="file-upload"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="file-upload">
            <Button
              variant="outlined"
              component="span"
              startIcon={<UploadIcon />}
              sx={{ mb: 2 }}
            >
              Select File
            </Button>
          </label>
          {selectedFile && (
            <Typography variant="body2" sx={{ ml: 1 }}>
              Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)} disabled={actionInProgress}>
            Cancel
          </Button>
          <Button 
            onClick={handleUploadFile} 
            variant="contained" 
            disabled={!selectedFile || actionInProgress}
          >
            {actionInProgress ? <CircularProgress size={24} /> : 'Upload'}
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

export default S3Page;