# Fix for Uploaded Images Not Displaying on PythonAnywhere

## The Problem
Images uploaded through the admin panel aren't showing up on your live PythonAnywhere site.

## The Solution

### Step 1: Update Your Code (DONE ✅)
The `admin.py` file has been updated to use absolute paths for uploads. This is already fixed in your local code.

### Step 2: Upload Updated Code to PythonAnywhere

**If using Git:**
```bash
# In PythonAnywhere Bash console
cd ~/PortfolioWebsite
git pull
```

**If uploading manually:**
- Upload the updated `admin.py` file via the Files tab

### Step 3: Verify Upload Folders Exist on PythonAnywhere

In PythonAnywhere Bash console:
```bash
cd ~/PortfolioWebsite
mkdir -p static/images/projects
mkdir -p static/readme
chmod 755 static/images/projects
chmod 755 static/readme
```

### Step 4: Configure Static File Mappings in PythonAnywhere

This is the CRITICAL step that's often missed!

1. Go to the **Web** tab in PythonAnywhere
2. Scroll to **Static files** section
3. Make sure you have this mapping:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/PortfolioWebsite/static/` |

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

The path MUST be absolute, like:
```
/home/gopalniraula/PortfolioWebsite/static/
```

### Step 5: Set Folder Permissions (Important!)

In PythonAnywhere Bash console:
```bash
cd ~/PortfolioWebsite
chmod -R 755 static
chmod -R 775 static/images/projects
chmod -R 775 static/readme
```

### Step 6: Reload Your Web App

1. Go to **Web** tab
2. Click the big green **Reload** button
3. Wait for reload to complete

### Step 7: Test Upload

1. Go to your admin panel: `yourusername.pythonanywhere.com/admin/login`
2. Add a new project with an image
3. Check if the image displays on the project page

## Quick Verification Commands

Run these in PythonAnywhere Bash console:

```bash
# Check if folders exist
ls -la ~/PortfolioWebsite/static/images/projects/

# Check permissions
ls -ld ~/PortfolioWebsite/static/images/projects/

# Upload a test file
cd ~/PortfolioWebsite/static/images/projects/
touch test.txt
ls -l test.txt

# If test.txt appears, permissions are OK
```

## Common Issues and Fixes

### Issue 1: Images upload but don't display

**Fix:** Check static file mapping in Web tab
- URL must be exactly: `/static/`
- Directory must be absolute: `/home/yourusername/PortfolioWebsite/static/`

### Issue 2: Can't upload files (error in admin)

**Fix:** Check folder permissions
```bash
cd ~/PortfolioWebsite
chmod -R 775 static/images/projects
chmod -R 775 static/readme
```

### Issue 3: Old images work, new ones don't

**Fix:** Reload the web app
- Go to Web tab → Click Reload
- Hard refresh browser: Ctrl+Shift+R (or Cmd+Shift+R on Mac)

### Issue 4: Images upload to wrong location

**Fix:** Verify the updated admin.py is deployed
```bash
cd ~/PortfolioWebsite
grep "BASE_DIR" admin.py
# Should show the absolute path code
```

## Debugging: Check Where Files Are Being Saved

Add this temporary debug code to see where uploads are going:

1. In PythonAnywhere, edit `admin.py`
2. Find the image upload section (around line 100)
3. Add a print statement:

```python
filepath = os.path.join(UPLOAD_FOLDER, filename)
print(f"DEBUG: Saving file to: {filepath}")  # Add this line
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
file.save(filepath)
```

4. Reload web app
5. Try uploading an image
6. Check Error log in Web tab for the DEBUG message
7. Remove the print statement after debugging

## Verify Your Setup

Check these in order:

- [ ] Updated `admin.py` uploaded to PythonAnywhere
- [ ] Upload folders exist: `static/images/projects/` and `static/readme/`
- [ ] Folder permissions are correct (755 or 775)
- [ ] Static file mapping configured: `/static/` → `/home/yourusername/PortfolioWebsite/static/`
- [ ] Web app reloaded after changes
- [ ] Browser cache cleared (Ctrl+Shift+R)

## Test That It's Working

1. **Test File Creation:**
   ```bash
   cd ~/PortfolioWebsite/static/images/projects/
   echo "test" > test.txt
   ```

2. **Test File Access:**
   Visit: `yourusername.pythonanywhere.com/static/images/projects/test.txt`
   
   Should show "test" in browser

3. **Test Image Upload:**
   - Login to admin
   - Create new project
   - Upload an image
   - Save project
   - View project page
   - Image should display

4. **Clean up test file:**
   ```bash
   rm ~/PortfolioWebsite/static/images/projects/test.txt
   ```

## Still Not Working?

### Check Error Logs
1. Web tab → Error log
2. Look for permission errors or path errors
3. Common error messages:
   - "Permission denied" → Fix folder permissions
   - "No such file or directory" → Check UPLOAD_FOLDER path
   - "404 on static file" → Check static file mapping

### Check Server Logs
1. Web tab → Server log
2. Look for any warnings about static files

### Manual Image Test
Upload an image manually and test:

```bash
cd ~/PortfolioWebsite/static/images/projects/
# Use Files tab to upload test.png here
ls -l test.png
```

Visit: `yourusername.pythonanywhere.com/static/images/projects/test.png`

If manual file works but upload doesn't:
- Check admin.py code is updated
- Check folder permissions are writable (775)
- Check web app was reloaded

## The Complete Fix (Summary)

```bash
# 1. Update code
cd ~/PortfolioWebsite
git pull  # or upload files manually

# 2. Create/verify folders
mkdir -p static/images/projects
mkdir -p static/readme

# 3. Set permissions
chmod -R 775 static/images/projects
chmod -R 775 static/readme

# 4. Configure static files in Web tab
# URL: /static/
# Directory: /home/yourusername/PortfolioWebsite/static/

# 5. Reload web app (click Reload button in Web tab)
```

After these steps, uploaded images should display correctly!

## Need More Help?

- Check PythonAnywhere help: https://help.pythonanywhere.com/
- Forum thread on file uploads: https://www.pythonanywhere.com/forums/
- Stack Overflow: Search "pythonanywhere flask file upload"
