/**
 * 格式化工具类
 * 提供各种数据格式化功能
 */

const format_utils = {
    /**
     * 格式化金额
     * @param {number} value - 金额数值
     * @param {string} currency - 货币代码，默认为CNY
     * @param {string} locale - 地区代码，默认为zh-CN
     * @returns {string} 格式化后的金额
     */
    formatCurrency(value, currency = 'CNY', locale = 'zh-CN') {
        if (value === null || value === undefined || isNaN(value)) {
            return '¥0.00';
        }

        try {
            return new Intl.NumberFormat(locale, {
                style: 'currency',
                currency: currency
            }).format(value);
        } catch (error) {
            console.error('格式化金额失败:', error);
            return `¥${value.toFixed(2)}`;
        }
    },

    /**
     * 格式化时间戳为日期字符串
     * @param {number|string|Date} timestamp - 时间戳
     * @param {string} locale - 地区代码，默认为zh-CN
     * @returns {string} 格式化后的日期时间
     */
    formatDate(timestamp, locale = 'zh-CN') {
        if (!timestamp) return '';

        try {
            const date = new Date(timestamp);
            if (isNaN(date.getTime())) {
                return '';
            }

            return new Intl.DateTimeFormat(locale, {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }).format(date);
        } catch (error) {
            console.error('格式化日期失败:', error);
            return new Date(timestamp).toLocaleString();
        }
    },

    /**
     * 格式化距离（公里）
     * @param {number} distance - 距离数值
     * @param {number} precision - 小数位数，默认为2
     * @returns {string} 格式化后的距离
     */
    formatDistance(distance, precision = 2) {
        if (distance === null || distance === undefined || isNaN(distance)) {
            return '0.00 km';
        }

        return `${distance.toFixed(precision)} km`;
    },

    /**
     * 格式化速度（公里/小时）
     * @param {number} speed - 速度数值
     * @param {number} precision - 小数位数，默认为2
     * @returns {string} 格式化后的速度
     */
    formatSpeed(speed, precision = 2) {
        if (speed === null || speed === undefined || isNaN(speed)) {
            return '0.00 km/h';
        }

        return `${speed.toFixed(precision)} km/h`;
    },

    /**
     * 格式化时间（分钟）
     * @param {number} minutes - 分钟数
     * @param {boolean} showSeconds - 是否显示秒数，默认为false
     * @returns {string} 格式化后的时间
     */
    formatTime(minutes, showSeconds = false) {
        if (minutes === null || minutes === undefined || isNaN(minutes)) {
            return '0分钟';
        }

        const hours = Math.floor(minutes / 60);
        const remainingMinutes = Math.floor(minutes % 60);
        const seconds = Math.floor((minutes % 1) * 60);

        let result = '';

        if (hours > 0) {
            result += `${hours}小时`;
        }

        if (remainingMinutes > 0) {
            result += `${remainingMinutes}分钟`;
        }

        if (showSeconds && seconds > 0) {
            result += `${seconds}秒`;
        }

        return result || '0分钟';
    },

    /**
     * 格式化百分比
     * @param {number} percentage - 百分比数值
     * @param {number} precision - 小数位数，默认为2
     * @returns {string} 格式化后的百分比
     */
    formatPercentage(percentage, precision = 2) {
        if (percentage === null || percentage === undefined || isNaN(percentage)) {
            return '0.00%';
        }

        return `${percentage.toFixed(precision)}%`;
    },

    /**
     * 格式化数据大小（字节转人类可读格式）
     * @param {number} size - 字节数
     * @param {number} precision - 小数位数，默认为2
     * @returns {string} 格式化后的数据大小
     */
    formatSize(size, precision = 2) {
        if (size === null || size === undefined || isNaN(size) || size === 0) {
            return '0 B';
        }

        const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const i = Math.floor(Math.log(size) / Math.log(1024));

        if (i >= units.length) {
            return `${(size / Math.pow(1024, units.length - 1)).toFixed(precision)} ${units[units.length - 1]}`;
        }

        return `${(size / Math.pow(1024, i)).toFixed(precision)} ${units[i]}`;
    },

    /**
     * 格式化IP地址
     * @param {string} ip - IP地址
     * @returns {string} 格式化后的IP地址
     */
    formatIpAddress(ip) {
        if (!ip || typeof ip !== 'string') {
            return '';
        }

        const parts = ip.split('.');
        if (parts.length !== 4) {
            return ip;
        }

        return parts.map(part => part.padStart(3, '0')).join('.');
    },

    /**
     * 格式化电子邮件地址
     * @param {string} email - 电子邮件地址
     * @param {number} visibleChars - 可见字符数，默认为3
     * @returns {string} 格式化后的电子邮件地址
     */
    formatEmail(email, visibleChars = 3) {
        if (!email || typeof email !== 'string') {
            return '';
        }

        const atIndex = email.indexOf('@');
        if (atIndex === -1) {
            return email;
        }

        const username = email.substring(0, atIndex);
        const domain = email.substring(atIndex);

        if (username.length <= visibleChars) {
            return email;
        }

        return `${username.substring(0, visibleChars)}...${domain}`;
    },

    /**
     * 格式化URL
     * @param {string} url - URL地址
     * @param {number} maxLength - 最大长度，默认为50
     * @returns {string} 格式化后的URL
     */
    formatUrl(url, maxLength = 50) {
        if (!url || typeof url !== 'string') {
            return '';
        }

        try {
            const urlObj = new URL(url);
            const domain = urlObj.hostname;
            const path = urlObj.pathname;

            const fullUrl = domain + path;
            if (fullUrl.length <= maxLength) {
                return fullUrl;
            }

            return `${fullUrl.substring(0, maxLength - 3)}...`;
        } catch (error) {
            // 如果不是有效的URL，直接截断
            return url.length <= maxLength ? url : `${url.substring(0, maxLength - 3)}...`;
        }
    },

    /**
     * 格式化日期时间（ISO 8601）
     * @param {number|string|Date} dateTime - 日期时间
     * @returns {string} ISO 8601格式的日期时间
     */
    formatDateTime(dateTime) {
        if (!dateTime) return '';

        try {
            return new Date(dateTime).toISOString();
        } catch (error) {
            console.error('格式化日期时间失败:', error);
            return '';
        }
    },

    /**
     * 格式化JSON数据
     * @param {any} json - JSON数据
     * @param {number} indent - 缩进空格数，默认为2
     * @returns {string} 格式化后的JSON字符串
     */
    formatJson(json, indent = 2) {
        try {
            return JSON.stringify(json, null, indent);
        } catch (error) {
            console.error('格式化JSON失败:', error);
            return '';
        }
    },

    /**
     * 格式化HTML特殊字符
     * @param {string} html - HTML字符串
     * @returns {string} 转义后的HTML字符串
     */
    formatHtml(html) {
        if (!html || typeof html !== 'string') {
            return '';
        }

        return html
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    },

    /**
     * 格式化电话号码
     * @param {string|number} phoneNumber - 电话号码
     * @param {string} format - 格式类型，默认为'default'
     * @returns {string} 格式化后的电话号码
     */
    formatPhoneNumber(phoneNumber, format = 'default') {
        if (!phoneNumber) return '';

        const cleaned = String(phoneNumber).replace(/\D/g, '');

        if (format === 'default') {
            // 默认格式：(xxx) xxx-xxxx
            const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
            if (match) {
                return `(${match[1]}) ${match[2]}-${match[3]}`;
            }
        } else if (format === 'chinese') {
            // 中国格式：xxx-xxxx-xxxx
            const match = cleaned.match(/^(\d{3})(\d{4})(\d{4})$/);
            if (match) {
                return `${match[1]}-${match[2]}-${match[3]}`;
            }
        }

        return phoneNumber;
    },

    /**
     * 格式化数字（添加千分位分隔符）
     * @param {number} number - 数字
     * @param {string} locale - 地区代码，默认为zh-CN
     * @returns {string} 格式化后的数字
     */
    formatNumber(number, locale = 'zh-CN') {
        if (number === null || number === undefined || isNaN(number)) {
            return '0';
        }

        try {
            return new Intl.NumberFormat(locale).format(number);
        } catch (error) {
            console.error('格式化数字失败:', error);
            return number.toString();
        }
    },

    /**
     * 格式化文件大小（人类可读格式）
     * @param {number} bytes - 字节数
     * @param {number} precision - 小数位数，默认为2
     * @returns {string} 格式化后的文件大小
     */
    formatFileSize(bytes, precision = 2) {
        return this.formatSize(bytes, precision);
    },

    /**
     * 格式化相对时间（如：2小时前）
     * @param {number|string|Date} date - 日期时间
     * @param {string} locale - 地区代码，默认为zh-CN
     * @returns {string} 格式化后的相对时间
     */
    formatRelativeTime(date, locale = 'zh-CN') {
        if (!date) return '';

        try {
            const now = new Date();
            const targetDate = new Date(date);
            const diffInSeconds = Math.floor((now - targetDate) / 1000);

            if (diffInSeconds < 60) {
                return '刚刚';
            } else if (diffInSeconds < 3600) {
                const minutes = Math.floor(diffInSeconds / 60);
                return `${minutes}分钟前`;
            } else if (diffInSeconds < 86400) {
                const hours = Math.floor(diffInSeconds / 3600);
                return `${hours}小时前`;
            } else if (diffInSeconds < 2592000) {
                const days = Math.floor(diffInSeconds / 86400);
                return `${days}天前`;
            } else {
                return this.formatDate(date, locale);
            }
        } catch (error) {
            console.error('格式化相对时间失败:', error);
            return '';
        }
    }
};

export { format_utils };
export default format_utils;



