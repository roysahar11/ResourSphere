// File: src/services/api.js

import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Default backend URL

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
    });
  }

  setToken(token) {
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  // Authentication
  async login(username, password) {
    const response = await this.api.post('/auth/login', { username, password });
    return response.data;
  }

  async getUserPermissions() {
    const response = await this.api.get('/auth/me');
    return response.data;
  }

  // EC2 Endpoints
  async createEC2Instance(name, instanceType, ami) {
    const response = await this.api.post('/ec2/create', {
      name,
      instance_type: instanceType,
      ami,
    });
    return response.data;
  }

  async listEC2Instances() {
    const response = await this.api.get('/ec2/list');
    return response.data.instances;
  }

  async startEC2Instance(instance) {
    const response = await this.api.post('/ec2/start', { instance });
    return response.data;
  }

  async stopEC2Instance(instance) {
    const response = await this.api.post('/ec2/stop', { instance });
    return response.data;
  }

  async deleteEC2Instance(instance) {
    const response = await this.api.delete('/ec2/delete', { 
      data: { instance } 
    });
    return response.data;
  }

  // S3 Endpoints
  async createS3Bucket(bucketName, publicAccess = false) {
    const response = await this.api.post('/s3/create', {
      bucket_name: bucketName,
      public_access: publicAccess,
    });
    return response.data;
  }

  async listS3Buckets() {
    const response = await this.api.get('/s3/list');
    return response.data.buckets;
  }

  async deleteS3Bucket(bucketName) {
    const response = await this.api.delete('/s3/delete', {
      data: { bucket_name: bucketName }
    });
    return response.data;
  }

  async uploadFileToS3(bucketName, file) {
    const formData = new FormData();
    formData.append('bucket_name', bucketName);
    formData.append('file', file);
    
    const response = await this.api.post('/s3/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // DNS Endpoints
  async createDNSZone(zoneName) {
    const response = await this.api.post('/route53/zone/create', {
      zone_name: zoneName,
    });
    return response.data;
  }

  async listDNSZones() {
    const response = await this.api.get('/route53/zones');
    return response.data;
  }
}

export default new ApiService();