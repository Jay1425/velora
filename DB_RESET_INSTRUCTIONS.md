# Database Schema Reset Instructions for Render

## Current Deployment Issue

Your production database has the **old schema** without the new order tracking fields (`order_number`, `status`, `updated_at`). The new code requires these fields to work.

## Solution: One-Time Database Reset

### Step 1: Add Environment Variable in Render

1. Go to your Render Dashboard: https://dashboard.render.com
2. Click on your Velora web service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   ```
   Key: RESET_DB
   Value: true
   ```
6. Click **Save Changes**

### Step 2: Deploy Will Auto-Trigger

Render will automatically redeploy when you save the environment variable.

During deployment, the app will:
- ✓ Drop all existing tables
- ✓ Create fresh tables with new schema
- ✓ All order tracking features will work

### Step 3: Remove Environment Variable (IMPORTANT!)

After successful deployment:

1. Go back to **Environment** tab
2. **DELETE** the `RESET_DB` variable
3. Save changes

**Why remove it?** 
- Leaving `RESET_DB=true` will drop your database on every deployment
- Removing it ensures data persists going forward

## Alternative: Manual Neon Console

If you prefer direct control:

1. Log into Neon: https://neon.tech
2. Go to your project → SQL Editor
3. Run:
   ```sql
   DROP TABLE IF EXISTS inquiry CASCADE;
   ```
4. Redeploy on Render (tables will be created automatically)

## Verification

After deployment, test:
1. Place an order at `/contact`
2. You should get an order number like `VEL-20260302-0001`
3. View order success page
4. Track order at `/track?order=VEL-20260302-0001`

## Future Migrations

For future schema changes, we can set up Flask-Migrate for safe migrations without data loss.

---

**Status**: Code deployed, waiting for `RESET_DB=true` environment variable to trigger reset.
