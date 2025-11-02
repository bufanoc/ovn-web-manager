import React, { useState, useEffect } from 'react';
import { Box, Typography, Grid, Paper, CircularProgress } from '@mui/material';
import { toast } from 'react-toastify';
import api from '../services/api';

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    switches: 0,
    routers: 0,
    ports: 0,
    acls: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [switchesRes, routersRes, portsRes, aclsRes] = await Promise.all([
          api.getLogicalSwitches(),
          api.getLogicalRouters(),
          api.getPorts(),
          api.getACLs()
        ]);

        setStats({
          switches: switchesRes.data?.length || 0,
          routers: routersRes.data?.length || 0,
          ports: portsRes.data?.length || 0,
          acls: aclsRes.data?.length || 0
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
        toast.error('Failed to load dashboard statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" color="primary">
              Logical Switches
            </Typography>
            <Typography variant="h3">{stats.switches}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" color="primary">
              Logical Routers
            </Typography>
            <Typography variant="h3">{stats.routers}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" color="primary">
              Ports
            </Typography>
            <Typography variant="h3">{stats.ports}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" color="primary">
              ACLs
            </Typography>
            <Typography variant="h3">{stats.acls}</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
