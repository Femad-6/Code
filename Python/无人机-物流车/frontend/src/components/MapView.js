import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import { Card, Button, Select, Space, Typography, message } from 'antd';
import { ReloadOutlined, FullscreenOutlined } from '@ant-design/icons';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

const { Title, Text } = Typography;
const { Option } = Select;

// 修复Leaflet默认图标问题
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// 自定义图标
const warehouseIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const deliveryIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const droneIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// 地图控制组件
const MapController = ({ center, zoom }) => {
    const map = useMap();

    useEffect(() => {
        if (center && zoom) {
            map.setView(center, zoom);
        }
    }, [center, zoom, map]);

    return null;
};

const MapView = ({
    center = [39.9042, 116.4074], // 默认北京坐标
    zoom = 10,
    markers = [],
    routes = [],
    deliveryPoints = [],
    warehouses = [],
    drones = [],
    onMarkerClick,
    onRouteClick,
    className = ""
}) => {
    const [mapCenter, setMapCenter] = useState(center);
    const [mapZoom, setMapZoom] = useState(zoom);
    const [selectedRoute, setSelectedRoute] = useState(null);
    const [showMarkers, setShowMarkers] = useState({
        delivery: true,
        warehouse: true,
        drone: true
    });

    // 处理标记点击
    const handleMarkerClick = (marker, type) => {
        if (onMarkerClick) {
            onMarkerClick(marker, type);
        }
    };

    // 处理路线点击
    const handleRouteClick = (route, index) => {
        setSelectedRoute(route);
        if (onRouteClick) {
            onRouteClick(route, index);
        }
    };

    // 刷新地图
    const handleRefresh = () => {
        setMapCenter(center);
        setMapZoom(zoom);
        message.success('地图已刷新');
    };

    // 全屏显示
    const handleFullscreen = () => {
        const mapElement = document.querySelector('.leaflet-container');
        if (mapElement.requestFullscreen) {
            mapElement.requestFullscreen();
        }
    };

    // 切换标记显示
    const handleMarkerToggle = (type, checked) => {
        setShowMarkers(prev => ({
            ...prev,
            [type]: checked
        }));
    };

    // 渲染配送点标记
    const renderDeliveryMarkers = () => {
        if (!showMarkers.delivery) return null;

        return deliveryPoints.map((point, index) => (
            <Marker
                key={`delivery-${point.id || index}`}
                position={[point.latitude, point.longitude]}
                icon={deliveryIcon}
                eventHandlers={{
                    click: () => handleMarkerClick(point, 'delivery')
                }}
            >
                <Popup>
                    <div className="marker-popup">
                        <Title level={5}>配送点</Title>
                        <Text strong>{point.name}</Text>
                        <br />
                        <Text type="secondary">{point.address}</Text>
                        {point.demand && (
                            <>
                                <br />
                                <Text>需求: {point.demand}kg</Text>
                            </>
                        )}
                    </div>
                </Popup>
            </Marker>
        ));
    };

    // 渲染仓库标记
    const renderWarehouseMarkers = () => {
        if (!showMarkers.warehouse) return null;

        return warehouses.map((warehouse, index) => (
            <Marker
                key={`warehouse-${warehouse.id || index}`}
                position={[warehouse.latitude, warehouse.longitude]}
                icon={warehouseIcon}
                eventHandlers={{
                    click: () => handleMarkerClick(warehouse, 'warehouse')
                }}
            >
                <Popup>
                    <div className="marker-popup">
                        <Title level={5}>仓库</Title>
                        <Text strong>{warehouse.name}</Text>
                        <br />
                        <Text type="secondary">{warehouse.address}</Text>
                    </div>
                </Popup>
            </Marker>
        ));
    };

    // 渲染无人机标记
    const renderDroneMarkers = () => {
        if (!showMarkers.drone) return null;

        return drones.map((drone, index) => (
            <Marker
                key={`drone-${drone.id || index}`}
                position={[drone.latitude, drone.longitude]}
                icon={droneIcon}
                eventHandlers={{
                    click: () => handleMarkerClick(drone, 'drone')
                }}
            >
                <Popup>
                    <div className="marker-popup">
                        <Title level={5}>无人机</Title>
                        <Text strong>{drone.registration_number}</Text>
                        <br />
                        <Text type="secondary">状态: {drone.status}</Text>
                        {drone.battery && (
                            <>
                                <br />
                                <Text>电池: {drone.battery}%</Text>
                            </>
                        )}
                    </div>
                </Popup>
            </Marker>
        ));
    };

    // 渲染路线
    const renderRoutes = () => {
        return routes.map((route, index) => (
            <Polyline
                key={`route-${index}`}
                positions={route.positions || route}
                color={route.color || '#1890ff'}
                weight={route.weight || 3}
                opacity={route.opacity || 0.7}
                eventHandlers={{
                    click: () => handleRouteClick(route, index)
                }}
            />
        ));
    };

    return (
        <div className={`map-view-container ${className}`}>
            <Card
                title={
                    <div className="map-header">
                        <Title level={4} style={{ margin: 0 }}>地图视图</Title>
                        <Space>
                            <Select
                                placeholder="显示选项"
                                mode="multiple"
                                value={Object.keys(showMarkers).filter(key => showMarkers[key])}
                                onChange={(values) => {
                                    const newShowMarkers = {};
                                    ['delivery', 'warehouse', 'drone'].forEach(key => {
                                        newShowMarkers[key] = values.includes(key);
                                    });
                                    setShowMarkers(newShowMarkers);
                                }}
                                style={{ width: 200 }}
                            >
                                <Option value="delivery">配送点</Option>
                                <Option value="warehouse">仓库</Option>
                                <Option value="drone">无人机</Option>
                            </Select>
                            <Button
                                icon={<ReloadOutlined />}
                                onClick={handleRefresh}
                                title="刷新地图"
                            />
                            <Button
                                icon={<FullscreenOutlined />}
                                onClick={handleFullscreen}
                                title="全屏显示"
                            />
                        </Space>
                    </div>
                }
                className="map-card"
            >
                <div className="map-container">
                    <MapContainer
                        center={mapCenter}
                        zoom={mapZoom}
                        className="leaflet-map"
                        zoomControl={true}
                    >
                        <MapController center={mapCenter} zoom={mapZoom} />

                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        />

                        {renderDeliveryMarkers()}
                        {renderWarehouseMarkers()}
                        {renderDroneMarkers()}
                        {renderRoutes()}
                    </MapContainer>
                </div>

                {selectedRoute && (
                    <div className="route-info">
                        <Title level={5}>路线信息</Title>
                        <Text>距离: {selectedRoute.distance || '未知'}km</Text>
                        <br />
                        <Text>预计时间: {selectedRoute.estimatedTime || '未知'}</Text>
                    </div>
                )}
            </Card>
        </div>
    );
};

export default MapView;



