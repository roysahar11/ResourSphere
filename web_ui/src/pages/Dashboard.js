// File: src/pages/Dashboard.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Paper,
  Button,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  Divider
} from '@mui/material';
import {
  Computer as ComputerIcon,
  Storage as StorageIcon,
  Language as LanguageIcon
} from '@mui/icons-material';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function Dashboard() {
  const { currentUser, userPermissions } = useAuth();
  const navigate = useNavigate();
  const [resourceCounts, setResourceCounts] = useState({
    ec2: { total: 0, running: 0 },
    s3: { total: 0 },
    dns: { total: 0 }
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResourceCounts();
  }, []);

  const fetchResourceCounts = async () => {
    setLoading(true);
    try {
      // Fetch EC2 instances
      const ec2Response = await api.listEC2Instances();
      const instances = ec2Response || [];
      const runningInstances = instances.filter(instance => instance.state === 'running');
      
      // Fetch S3 buckets
      const s3Response = await api.listS3Buckets();
      const buckets = s3Response || [];
      
      // Fetch DNS zones
      const dnsResponse = await api.listDNSZones();
      const zones = dnsResponse.zones || [];
      
      setResourceCounts({
        ec2: { 
          total: instances.length,
          running: runningInstances.length
        },
        s3: { total: buckets.length },
        dns: { total: zones.length }
      });
    } catch (error) {
      console.error('Failed to fetch resource counts:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome, {currentUser}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage your AWS resources with ResourSphere
        </Typography>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 140,
                  bgcolor: 'primary.light',
                  color: 'white'
                }}
              >
                <Typography component="h2" variant="h6" gutterBottom>
                  EC2 Instances
                </Typography>
                <Typography component="p" variant="h4">
                  {resourceCounts.ec2.total}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {resourceCounts.ec2.running} running instances
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 140,
                  bgcolor: 'secondary.light',
                  color: 'white'
                }}
              >
                <Typography component="h2" variant="h6" gutterBottom>
                  S3 Buckets
                </Typography>
                <Typography component="p" variant="h4">
                  {resourceCounts.s3.total}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Total storage buckets
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 140,
                  bgcolor: 'info.light',
                  color: 'white'
                }}
              >
                <Typography component="h2" variant="h6" gutterBottom>
                  DNS Zones
                </Typography>
                <Typography component="p" variant="h4">
                  {resourceCounts.dns.total}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Managed DNS zones
                </Typography>
              </Paper>
            </Grid>
          </Grid>

          <Typography variant="h5" sx={{ mb: 3 }}>
            Quick Actions
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ComputerIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6">EC2 Instances</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Create and manage virtual servers in the cloud.
                  </Typography>
                </CardContent>
                <Divider />
                <CardActions>
                  <Button size="small" onClick={() => navigate('/ec2')}>Manage Instances</Button>
                  <Button 
                    size="small" 
                    color="primary" 
                    onClick={() => navigate('/ec2')}
                  >
                    Create New
                  </Button>
                </CardActions>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <StorageIcon sx={{ mr: 1, color: 'secondary.main' }} />
                    <Typography variant="h6">S3 Storage</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Store and retrieve data from scalable cloud storage.
                  </Typography>
                </CardContent>
                <Divider />
                <CardActions>
                  <Button size="small" onClick={() => navigate('/s3')}>Manage Buckets</Button>
                  <Button 
                    size="small" 
                    color="secondary" 
                    onClick={() => navigate('/s3')}
                  >
                    Create New
                  </Button>
                </CardActions>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <LanguageIcon sx={{ mr: 1, color: 'info.main' }} />
                    <Typography variant="h6">DNS Management</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Create and manage DNS zones and records.
                  </Typography>
                </CardContent>
                <Divider />
                <CardActions>
                  <Button size="small" onClick={() => navigate('/dns')}>Manage Zones</Button>
                  <Button 
                    size="small" 
                    color="info" 
                    onClick={() => navigate('/dns')}
                  >
                    Create New
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </Grid>
        </>
      )}
    </Container>
  );
}

export default Dashboard;