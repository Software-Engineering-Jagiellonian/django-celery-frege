import type { Metadata } from 'next';
import './globals.css';
import NavigationBar from './layoutComponents';

export const metadata: Metadata = {
  title: 'Frege'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <NavigationBar>{children} </NavigationBar>
      </body>
    </html>
  );
}
